import os

from django.utils.text import slugify

from rest_framework import serializers

from .models import (
    Announcement,
    AnnouncementComment,
    AnnouncementCommentLike,
    AnnouncementDeck,
    AnnouncementDeckItem,
    AnnouncementLike,
    AuditLogEntry,
    Attendance,
    ChurchBiography,
    ChurchConsistory,
    Contact,
    Department,
    Document,
    Event,
    EventComment,
    EventAttendanceAggregate,
    EventVisitorAggregate,
    EventLogisticsConsumption,
    BaptismEvent,
    BaptismCandidate,
    EvangelismActivity,
    TrainingEvent,
    MarriageRecord,
    Family,
    FinancialCategory,
    FinancialTransaction,
    HomeGroup,
    Member,
    Ministry,
    ActivityDuration,
    LogisticsItem,
    Notification,
    ApprovalRequest,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    department_id = serializers.SerializerMethodField(read_only=True)
    department_name = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    def get_department_id(self, obj):
        try:
            member = getattr(obj, 'member', None)
            dep = getattr(member, 'department', None) if member else None
            return getattr(dep, 'id', None)
        except Exception:
            return None

    def get_department_name(self, obj):
        try:
            member = getattr(obj, 'member', None)
            dep = getattr(member, 'department', None) if member else None
            return getattr(dep, 'name', None)
        except Exception:
            return None

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
            'is_staff',
            'role',
            'department_id',
            'department_name',
            'phone',
            'photo',
            'password',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class MeUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=False)
    current_password = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(required=False, allow_blank=False)
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        if not user or not getattr(user, 'is_authenticated', False):
            raise serializers.ValidationError('Non authentifié.')

        username = attrs.get('username')
        new_password = attrs.get('new_password')
        wants_sensitive = (username is not None) or (new_password is not None)

        if wants_sensitive:
            current_password = attrs.get('current_password')
            if not current_password or not user.check_password(current_password):
                raise serializers.ValidationError({'current_password': 'Mot de passe actuel incorrect.'})

        username = attrs.get('username')
        if username is not None:
            username = str(username).strip()
            if not username:
                raise serializers.ValidationError({'username': 'Nom d’utilisateur invalide.'})
            if User.objects.exclude(id=user.id).filter(username=username).exists():
                raise serializers.ValidationError({'username': 'Nom d’utilisateur déjà utilisé.'})
            attrs['username'] = username

        new_password = attrs.get('new_password')
        if new_password is not None:
            new_password = str(new_password)
            if len(new_password) < 6:
                raise serializers.ValidationError({'new_password': 'Mot de passe trop court.'})
            attrs['new_password'] = new_password

        if 'first_name' in attrs:
            attrs['first_name'] = str(attrs.get('first_name') or '').strip()

        if 'last_name' in attrs:
            attrs['last_name'] = str(attrs.get('last_name') or '').strip()

        if (
            attrs.get('username') is None
            and attrs.get('new_password') is None
            and attrs.get('photo') is None
            and attrs.get('first_name') is None
            and attrs.get('last_name') is None
        ):
            raise serializers.ValidationError('Aucune modification demandée.')

        return attrs

    def save(self, **kwargs):
        request = self.context.get('request')
        user = request.user
        update_fields = []

        username = self.validated_data.get('username')
        if username is not None and username != user.username:
            user.username = username
            update_fields.append('username')

        new_password = self.validated_data.get('new_password')
        if new_password is not None:
            user.set_password(new_password)
            update_fields.append('password')

        first_name = self.validated_data.get('first_name')
        if first_name is not None and first_name != user.first_name:
            user.first_name = first_name
            update_fields.append('first_name')

        last_name = self.validated_data.get('last_name')
        if last_name is not None and last_name != user.last_name:
            user.last_name = last_name
            update_fields.append('last_name')

        photo = self.validated_data.get('photo')
        if photo is not None:
            user.photo = photo
            update_fields.append('photo')

        if update_fields:
            user.save(update_fields=update_fields)
        return user


class ActivityDurationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ActivityDuration
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        label = str(attrs.get('label') or '').strip()
        if not label:
            raise serializers.ValidationError({'label': 'Libellé requis.'})
        attrs['label'] = label

        if self.instance is not None:
            code_in = attrs.get('code')
            if code_in is None or not str(code_in).strip():
                attrs['code'] = self.instance.code
                return attrs

        code = str(attrs.get('code') or '').strip()
        if not code:
            base = slugify(label) or 'duration'
            code = base
            i = 1
            while ActivityDuration.objects.filter(code=code).exists():
                i += 1
                code = f"{base}-{i}"

        qs = ActivityDuration.objects.filter(code=code)
        if self.instance is not None:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError({'code': 'Code déjà utilisé.'})
        attrs['code'] = code
        return attrs


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class HomeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeGroup
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'member_number')


class EventSerializer(serializers.ModelSerializer):
    special_details = serializers.SerializerMethodField(read_only=True)

    def get_special_details(self, obj):
        et = getattr(obj, 'event_type', None)
        if et == 'training':
            te = getattr(obj, 'training_event', None)
            if not te:
                return None
            return {
                'type': 'training',
                'trainer': getattr(te, 'trainer', None),
                'lesson': getattr(te, 'lesson', None),
            }
        if et == 'evangelism':
            ea = getattr(obj, 'evangelism_activity', None)
            if not ea:
                return None
            return {
                'type': 'evangelism',
                'activity_type': getattr(ea, 'activity_type', None),
                'moderator': getattr(ea, 'moderator', None) or getattr(obj, 'moderator', None),
            }
        if et == 'baptism':
            be = getattr(obj, 'baptism_event', None)
            if not be:
                return None
            try:
                cand_count = getattr(be, 'candidates', None).count()
            except Exception:
                cand_count = None
            return {
                'type': 'baptism',
                'moderator': getattr(obj, 'moderator', None),
                'executors': getattr(be, 'executors', None) or [],
                'candidates_count': cand_count,
            }
        return None

    class Meta:
        model = Event
        fields = '__all__'


class EventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'event')


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class EventAttendanceAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendanceAggregate
        fields = '__all__'
        read_only_fields = ('id', 'event', 'updated_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        for k in ('male_adults', 'female_adults', 'male_children', 'female_children'):
            v = attrs.get(k)
            if v is None:
                continue
            try:
                if int(v) < 0:
                    raise serializers.ValidationError({k: 'Valeur invalide.'})
            except (TypeError, ValueError):
                raise serializers.ValidationError({k: 'Valeur invalide.'})
        return attrs


class BaptismEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True, required=False)
    title = serializers.CharField(write_only=True, required=False, allow_blank=True)
    date = serializers.DateField(write_only=True, required=False)
    time = serializers.TimeField(write_only=True, required=False)
    location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    moderator = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def create(self, validated_data):
        # These fields are used only to create/update the linked Event in the ViewSet.
        validated_data.pop('title', None)
        validated_data.pop('date', None)
        validated_data.pop('time', None)
        validated_data.pop('location', None)
        validated_data.pop('moderator', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('title', None)
        validated_data.pop('date', None)
        validated_data.pop('time', None)
        validated_data.pop('location', None)
        validated_data.pop('moderator', None)
        return super().update(instance, validated_data)

    class Meta:
        model = BaptismEvent
        fields = '__all__'


class BaptismCandidateSerializer(serializers.ModelSerializer):
    baptism_event_id = serializers.PrimaryKeyRelatedField(queryset=BaptismEvent.objects.all(), source='baptism_event', write_only=True, required=False)

    class Meta:
        model = BaptismCandidate
        fields = '__all__'
        extra_kwargs = {
            'baptism_event': {'required': False},
        }


class EvangelismActivitySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        activity_type = attrs.get('activity_type')
        if activity_type is None and self.instance is not None:
            activity_type = getattr(self.instance, 'activity_type', None)

        if activity_type == 'other':
            custom = attrs.get('custom_activity_type')
            if custom is None and self.instance is not None:
                custom = getattr(self.instance, 'custom_activity_type', None)
            if not str(custom or '').strip():
                raise serializers.ValidationError({'custom_activity_type': "Renseigne le type d'activité."})

        return super().validate(attrs)

    class Meta:
        model = EvangelismActivity
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')


class TrainingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingEvent
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')


class MarriageRecordSerializer(serializers.ModelSerializer):
    groom_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='groom', write_only=True, required=False, allow_null=True)
    bride_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='bride', write_only=True, required=False, allow_null=True)
    groom_name = serializers.SerializerMethodField(read_only=True)
    bride_name = serializers.SerializerMethodField(read_only=True)
    published_event_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MarriageRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at', 'published_event')

    def validate(self, attrs):
        groom = attrs.get('groom')
        bride = attrs.get('bride')

        groom_full_name = attrs.get('groom_full_name')
        bride_full_name = attrs.get('bride_full_name')

        if groom_full_name is None and self.instance is not None:
            groom_full_name = getattr(self.instance, 'groom_full_name', None)
        if bride_full_name is None and self.instance is not None:
            bride_full_name = getattr(self.instance, 'bride_full_name', None)

        if groom is None and self.instance is not None:
            groom = getattr(self.instance, 'groom', None)
        if bride is None and self.instance is not None:
            bride = getattr(self.instance, 'bride', None)

        if not (groom or str(groom_full_name or '').strip()):
            raise serializers.ValidationError({'groom_full_name': 'Nom du marié requis.'})
        if not (bride or str(bride_full_name or '').strip()):
            raise serializers.ValidationError({'bride_full_name': 'Nom de la mariée requis.'})

        return attrs

    def get_groom_name(self, obj):
        fallback = (getattr(obj, 'groom_full_name', None) or '').strip() or None
        m = getattr(obj, 'groom', None)
        u = getattr(m, 'user', None) if m else None
        return (u.get_full_name() if u else '').strip() or (u.username if u else None) or (getattr(m, 'member_number', None) if m else None) or fallback

    def get_bride_name(self, obj):
        fallback = (getattr(obj, 'bride_full_name', None) or '').strip() or None
        m = getattr(obj, 'bride', None)
        u = getattr(m, 'user', None) if m else None
        return (u.get_full_name() if u else '').strip() or (u.username if u else None) or (getattr(m, 'member_number', None) if m else None) or fallback


class EventVisitorAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVisitorAggregate
        fields = '__all__'
        read_only_fields = ('id', 'event', 'updated_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        for k in ('male_visitors', 'female_visitors'):
            v = attrs.get(k)
            if v is None:
                continue
            try:
                if int(v) < 0:
                    raise serializers.ValidationError({k: 'Valeur invalide.'})
            except (TypeError, ValueError):
                raise serializers.ValidationError({k: 'Valeur invalide.'})
        return attrs


class EventLogisticsConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLogisticsConsumption
        fields = '__all__'
        read_only_fields = ('id', 'event', 'updated_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        qty = attrs.get('quantity_used')
        if qty is None:
            return attrs
        try:
            if int(qty) < 0:
                raise serializers.ValidationError({'quantity_used': 'Valeur invalide.'})
        except (TypeError, ValueError):
            raise serializers.ValidationError({'quantity_used': 'Valeur invalide.'})
        return attrs


class FinancialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCategory
        fields = '__all__'


class FinancialTransactionSerializer(serializers.ModelSerializer):
    cashier_name = serializers.SerializerMethodField(read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FinancialTransaction
        fields = '__all__'
        extra_kwargs = {
            'document_number': {'read_only': True},
            'receipt_code': {'read_only': True},
            'receipt_pdf': {'read_only': True},
            'receipt_sent_at': {'read_only': True},
            'cashier': {'read_only': True},
            'created_by': {'read_only': True},
        }

    def validate(self, attrs):
        direction = attrs.get('direction')
        if not direction and self.instance is not None:
            direction = getattr(self.instance, 'direction', None)

        if direction == 'out':
            proof = attrs.get('proof_image')
            if proof is None and self.instance is not None:
                proof = getattr(self.instance, 'proof_image', None)
            if not proof:
                raise serializers.ValidationError({'proof_image': 'Une preuve (photo) est requise pour une sortie.'})

            recipient_name = attrs.get('recipient_name')
            if recipient_name is None and self.instance is not None:
                recipient_name = getattr(self.instance, 'recipient_name', None)
            if not recipient_name:
                raise serializers.ValidationError({'recipient_name': 'Le nom du destinataire est requis pour une sortie.'})

            recipient_email = attrs.get('recipient_email')
            if recipient_email is None and self.instance is not None:
                recipient_email = getattr(self.instance, 'recipient_email', None)
            if not recipient_email:
                raise serializers.ValidationError({'recipient_email': "L'email du destinataire est requis pour une sortie."})

            recipient_phone = attrs.get('recipient_phone')
            if recipient_phone is None and self.instance is not None:
                recipient_phone = getattr(self.instance, 'recipient_phone', None)
            if not recipient_phone:
                raise serializers.ValidationError({'recipient_phone': 'Le téléphone du destinataire est requis pour une sortie.'})

        return attrs

    def get_cashier_name(self, obj):
        user = getattr(obj, 'cashier', None)
        if not user:
            return None
        name = (f"{user.first_name} {user.last_name}").strip()
        return name or getattr(user, 'username', None)

    def get_created_by_name(self, obj):
        user = getattr(obj, 'created_by', None)
        if not user:
            return None
        name = (f"{user.first_name} {user.last_name}").strip()
        return name or getattr(user, 'username', None)


class AuditLogEntrySerializer(serializers.ModelSerializer):
    actor_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AuditLogEntry
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_actor_username(self, obj):
        actor = getattr(obj, 'actor', None)
        return getattr(actor, 'username', None) if actor else None


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    liked_by_me = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = (
            'id',
            'author',
            'published_date',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'title': {'required': False, 'allow_blank': True},
            'content': {'required': False, 'allow_blank': True},
            'author': {'read_only': True},
            'published_date': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, attrs):
        title = attrs.get('title')
        content = attrs.get('content')
        image = attrs.get('image')

        if title is None and self.instance is not None:
            title = getattr(self.instance, 'title', None)
        if content is None and self.instance is not None:
            content = getattr(self.instance, 'content', None)
        if image is None and self.instance is not None:
            image = getattr(self.instance, 'image', None)

        if not (str(title or '').strip() or str(content or '').strip() or image):
            raise serializers.ValidationError('Publication vide. Ajoute un titre, un texte ou une image.')

        return attrs

    def get_author_name(self, obj):
        user = getattr(obj, 'author', None)
        if not user:
            return None
        name = (f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}").strip()
        return name or getattr(user, 'username', None)

    def get_like_count(self, obj):
        return getattr(obj, 'likes', None).count() if getattr(obj, 'likes', None) is not None else 0

    def get_comment_count(self, obj):
        return getattr(obj, 'comments', None).count() if getattr(obj, 'comments', None) is not None else 0

    def get_liked_by_me(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        user = getattr(request, 'user', None) if request else None
        if not user or not user.is_authenticated:
            return False
        return AnnouncementLike.objects.filter(announcement=obj, user=user).exists()


class AnnouncementCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    liked_by_me = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnnouncementComment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'announcement', 'author')

    def get_author_name(self, obj):
        user = getattr(obj, 'author', None)
        if not user:
            return '—'
        name = (f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}").strip()
        return name or getattr(user, 'username', None) or '—'

    def get_like_count(self, obj):
        return getattr(obj, 'likes', None).count() if getattr(obj, 'likes', None) is not None else 0

    def get_liked_by_me(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        user = getattr(request, 'user', None) if request else None
        if not user or not user.is_authenticated:
            return False
        return AnnouncementCommentLike.objects.filter(comment=obj, user=user).exists()


class AnnouncementDeckItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementDeckItem
        fields = '__all__'
        read_only_fields = ('id', 'deck', 'created_at', 'updated_at')


class AnnouncementDeckSerializer(serializers.ModelSerializer):
    items = AnnouncementDeckItemSerializer(many=True, read_only=True)
    event_title = serializers.SerializerMethodField(read_only=True)
    event_date = serializers.SerializerMethodField(read_only=True)
    event_time = serializers.SerializerMethodField(read_only=True)
    event_location = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnnouncementDeck
        fields = '__all__'
        read_only_fields = ('id', 'pptx_file', 'generated_at', 'created_by', 'created_at', 'updated_at')

    def get_event_title(self, obj):
        ev = getattr(obj, 'event', None)
        return getattr(ev, 'title', None) if ev else None

    def get_event_date(self, obj):
        ev = getattr(obj, 'event', None)
        return getattr(ev, 'date', None) if ev else None

    def get_event_time(self, obj):
        ev = getattr(obj, 'event', None)
        return getattr(ev, 'time', None) if ev else None

    def get_event_location(self, obj):
        ev = getattr(obj, 'event', None)
        return getattr(ev, 'location', None) if ev else None


class DocumentSerializer(serializers.ModelSerializer):
    MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'}

    class Meta:
        model = Document
        fields = (
            'id',
            'title',
            'document_type',
            'file',
            'uploaded_by',
            'uploaded_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'uploaded_by', 'uploaded_at', 'created_at', 'updated_at')

    def validate_title(self, value):
        title = str(value or '').strip()
        if not title:
            raise serializers.ValidationError('Le nom du document est requis.')
        return title

    def validate(self, attrs):
        attrs = super().validate(attrs)

        file = attrs.get('file')
        title = attrs.get('title')

        if self.instance is None:
            if not file:
                raise serializers.ValidationError({'file': 'Fichier requis.'})

        if file is not None:
            original_name = getattr(file, 'name', '') or ''
            ext = os.path.splitext(original_name)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise serializers.ValidationError({'file': 'Formats acceptés: PDF, Word, Excel, PowerPoint.'})

            size = getattr(file, 'size', None)
            if size is not None and int(size) > int(self.MAX_UPLOAD_SIZE_BYTES):
                max_mb = round(self.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024), 1)
                raise serializers.ValidationError({'file': f'Fichier trop volumineux. Taille maximale: {max_mb} MB.'})

            safe = slugify(title or '')
            if not safe:
                safe = 'document'
            file.name = f'{safe}{ext}'
            attrs['file'] = file

        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ApprovalRequestSerializer(serializers.ModelSerializer):
    requested_by_username = serializers.SerializerMethodField(read_only=True)
    decided_by_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = '__all__'

    def get_requested_by_username(self, obj):
        u = getattr(obj, 'requested_by', None)
        return getattr(u, 'username', None) if u else None

    def get_decided_by_username(self, obj):
        u = getattr(obj, 'decided_by', None)
        return getattr(u, 'username', None) if u else None


class LogisticsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'asset_tag', 'purchase_price')

    def validate(self, attrs):
        if 'asset_tag' in attrs:
            attrs.pop('asset_tag', None)

        if 'purchase_price' in attrs:
            attrs.pop('purchase_price', None)

        name = attrs.get('name')
        if name is None and self.instance is not None:
            name = getattr(self.instance, 'name', None)
        if not str(name or '').strip():
            raise serializers.ValidationError({'name': 'Le nom du matériel est requis.'})

        currency = attrs.get('purchase_currency')
        if currency is None and self.instance is not None:
            currency = getattr(self.instance, 'purchase_currency', None)
        if currency is not None:
            currency = str(currency).strip().upper()
            if currency not in {'CDF', 'USD'}:
                raise serializers.ValidationError({'purchase_currency': 'Devise invalide. Utilisez CDF ou USD.'})
            attrs['purchase_currency'] = currency

        unit_price = attrs.get('unit_price')
        if unit_price is None and self.instance is not None:
            unit_price = getattr(self.instance, 'unit_price', None)
        if unit_price is not None:
            try:
                if float(unit_price) < 0:
                    raise serializers.ValidationError({'unit_price': 'Le prix unitaire doit être positif.'})
            except (TypeError, ValueError):
                raise serializers.ValidationError({'unit_price': 'Prix unitaire invalide.'})

        qty = attrs.get('quantity')
        if qty is None and self.instance is not None:
            qty = getattr(self.instance, 'quantity', None)
        if qty is None:
            return attrs
        try:
            if int(qty) <= 0:
                raise serializers.ValidationError({'quantity': 'La quantité doit être supérieure à 0.'})
        except (TypeError, ValueError):
            raise serializers.ValidationError({'quantity': 'Quantité invalide.'})

        return attrs


class ChurchBiographySerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChurchBiography
        fields = (
            'id', 'title', 'content', 'address', 'phone', 'email',
            'facebook_url', 'youtube_url', 'instagram_url', 'service_times',
            'is_active', 'created_at', 'updated_at', 'created_by', 'created_by_username'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def get_created_by_username(self, obj):
        u = getattr(obj, 'created_by', None)
        return getattr(u, 'username', None) if u else None


class ChurchConsistorySerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChurchConsistory
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def get_created_by_username(self, obj):
        u = getattr(obj, 'created_by', None)
        return getattr(u, 'username', None) if u else None


class ContactSerializer(serializers.ModelSerializer):
    """Serializer pour les messages de contact"""
    answered_by_username = serializers.SerializerMethodField(read_only=True)
    subject_label = serializers.SerializerMethodField(read_only=True)
    status_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contact
        fields = (
            'id', 'name', 'email', 'phone', 'subject', 'subject_label',
            'message', 'status', 'status_label', 'notes', 'answered_by',
            'answered_by_username', 'answered_at', 'ip_address', 'user_agent',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'ip_address', 'user_agent', 'answered_at')

    def get_answered_by_username(self, obj):
        u = getattr(obj, 'answered_by', None)
        return getattr(u, 'username', None) if u else None

    def get_subject_label(self, obj):
        return dict(Contact.SUBJECT_CHOICES).get(obj.subject, obj.subject)

    def get_status_label(self, obj):
        return dict(Contact.STATUS_CHOICES).get(obj.status, obj.status)

    def validate(self, attrs):
        # Valider le nom
        name = attrs.get('name')
        if name:
            attrs['name'] = str(name).strip()
        
        # Valider l'email
        email = attrs.get('email')
        if email:
            attrs['email'] = str(email).strip().lower()
        
        # Valider le message
        message = attrs.get('message')
        if message and len(str(message).strip()) < 10:
            raise serializers.ValidationError({'message': 'Le message doit contenir au moins 10 caractères.'})
        
        return attrs

