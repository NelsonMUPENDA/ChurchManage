from decimal import Decimal, InvalidOperation

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('pastor', 'Pastor'),
        ('admin', 'Administrator'),
        ('administrator', 'Administrator'),
        ('protocol_head', 'Protocol Head'),
        ('financial_head', 'Financial Head'),
        ('logistics_head', 'Logistics Head'),
        ('evangelism_head', 'Evangelism Head'),
        ('department_head', 'Department Head'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretary'),
        ('member', 'Member'),
        ('visitor', 'Visitor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    INACTIVE_REASON_CHOICES = [
        ('deceased', 'Décédé'),
        ('excluded', 'Exclu'),
        ('resigned', 'Démissionné'),
        ('transferred', 'Transféré'),
        ('absent', 'Absent prolongé'),
        ('other', 'Autre'),
    ]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    member_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    post_name = models.CharField(max_length=120, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=120, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=80, blank=True, null=True)
    marital_status = models.CharField(max_length=30, blank=True, null=True)
    occupation = models.CharField(max_length=120, blank=True, null=True)
    public_function = models.CharField(max_length=120, blank=True, null=True)
    church_position = models.CharField(max_length=120, blank=True, null=True)
    education_level = models.CharField(max_length=120, blank=True, null=True)
    father_full_name = models.CharField(max_length=150, blank=True, null=True)
    mother_full_name = models.CharField(max_length=150, blank=True, null=True)
    province = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    commune = models.CharField(max_length=80, blank=True, null=True)
    quarter = models.CharField(max_length=120, blank=True, null=True)
    avenue = models.CharField(max_length=120, blank=True, null=True)
    house_number = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=60, blank=True, null=True)
    baptism_date = models.DateField(blank=True, null=True)
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
    home_group = models.ForeignKey('HomeGroup', on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
    ministry = models.ForeignKey('Ministry', on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
    is_active = models.BooleanField(default=True)
    inactive_reason = models.CharField(max_length=30, choices=INACTIVE_REASON_CHOICES, blank=True, null=True)
    archived_date = models.DateTimeField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/members/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        """Retourne le nom complet du membre"""
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.member_number or "Membre inconnu"

    def save(self, *args, **kwargs):
        # Générer le numéro de membre si nécessaire
        is_new = not self.pk
        super().save(*args, **kwargs)
        
        if not self.member_number:
            self.member_number = f"CPD-MEM-{self.pk:06d}"
            super().save(update_fields=['member_number'])
        
        # Générer le QR code pour les nouveaux membres ou si absent
        if is_new or not self.qr_code:
            self._generate_qr_code()
            super().save(update_fields=['qr_code'])
    
    def _generate_qr_code(self):
        """Génère un QR code unique pour le membre"""
        import qrcode
        from io import BytesIO
        from django.core.files import File
        import os
        
        # Données à encoder dans le QR code
        qr_data = f"MEMBER:{self.member_number}|ID:{self.pk}|CHURCH:CPD"
        
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Générer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder dans un buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Créer le fichier Django
        filename = f"member_{self.member_number.replace('-', '_')}.png"
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

class Family(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HomeGroup(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='led_groups')
    meeting_day = models.CharField(max_length=20, blank=True, null=True)
    meeting_time = models.TimeField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='headed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    leader = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='led_ministries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ActivityDuration(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('service', 'Service'),
        ('meeting', 'Meeting'),
        ('special', 'Special Event'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('weekly_service', 'Culte hebdomadaire'),
        ('sunday_service', 'Culte dominical'),
        ('seminar', 'Séminaire'),
        ('mothers_teaching', 'Enseignement des mamans'),
        ('fathers_teaching', 'Enseignement des papas'),
        ('youth_service', 'Culte des jeunes'),
        ('department_meeting', 'Rencontre de département'),
        ('baptism', 'Baptême'),
        ('evangelism', 'Évangélisation'),
        ('training', 'Formation'),
        ('marriage', 'Mariage'),
    ]
    DURATION_CHOICES = [
        ('daily', 'Journalière'),
        ('weekly', 'Hebdomadaire'),
        ('21d', '21 jours'),
        ('40d', '40 jours'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='service')
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, default='daily')
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField(blank=True, null=True)
    moderator = models.CharField(max_length=150, blank=True, null=True)
    preacher = models.CharField(max_length=150, blank=True, null=True)
    choir = models.CharField(max_length=150, blank=True, null=True)
    protocol_team = models.CharField(max_length=150, blank=True, null=True)
    tech_team = models.CharField(max_length=150, blank=True, null=True)
    communicator = models.CharField(max_length=150, blank=True, null=True)
    poster_image = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    closure_validated_at = models.DateTimeField(blank=True, null=True)
    is_alert = models.BooleanField(default=False)
    alert_message = models.CharField(max_length=255, blank=True, null=True)
    share_slug = models.CharField(max_length=64, unique=True, blank=True, null=True)
    responsible = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='responsible_events')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=150, blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    attended = models.BooleanField(default=False)
    qr_code = models.CharField(max_length=100, blank=True, null=True)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventAttendanceAggregate(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='attendance_aggregate')

    # Adultes
    male_adults = models.PositiveIntegerField(default=0, verbose_name="Hommes adultes")
    female_adults = models.PositiveIntegerField(default=0, verbose_name="Femmes adultes")

    # Jeunes
    young_men = models.PositiveIntegerField(default=0, verbose_name="Jeunes hommes (garçons)")
    young_women = models.PositiveIntegerField(default=0, verbose_name="Jeunes filles")

    # Enfants
    male_children = models.PositiveIntegerField(default=0, verbose_name="Garçons (enfants)")
    female_children = models.PositiveIntegerField(default=0, verbose_name="Filles (enfants)")
    children_total = models.PositiveIntegerField(default=0, verbose_name="Total enfants")

    # Personnes âgées
    elderly_men = models.PositiveIntegerField(default=0, verbose_name="Hommes âgés (papas/vieillards)")
    elderly_women = models.PositiveIntegerField(default=0, verbose_name="Femmes âgées (mamas)")

    # Totaux calculés
    total_men = models.PositiveIntegerField(default=0, verbose_name="Total hommes")
    total_women = models.PositiveIntegerField(default=0, verbose_name="Total femmes")
    grand_total = models.PositiveIntegerField(default=0, verbose_name="Total général")

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_event_attendance_aggregates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_totals(self):
        """Calcule les totaux automatiquement"""
        self.total_men = self.male_adults + self.young_men + self.male_children + self.elderly_men
        self.total_women = self.female_adults + self.young_women + self.female_children + self.elderly_women
        self.children_total = self.male_children + self.female_children
        self.grand_total = self.total_men + self.total_women
        return self.grand_total

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)


class EventVisitorAggregate(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='visitor_aggregate')
    male_visitors = models.PositiveIntegerField(default=0)
    female_visitors = models.PositiveIntegerField(default=0)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_event_visitor_aggregates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FinancialCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FinancialDocumentSequence(models.Model):
    prefix = models.CharField(max_length=4)
    year = models.PositiveIntegerField()
    last_number = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('prefix', 'year')

class FinancialTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('offering', 'Offrandes'),
        ('tithe', 'Dîmes'),
        ('special_donation', 'Don spécial'),
        ('project_fund', 'Fonds projet'),
        ('thanksgiving', 'Actions de grâce'),
        ('construction', 'Construction'),
        ('donation', 'Don'),
        ('seed_vow', 'Semences et Vœux'),
        ('gift_other', 'Dons et autres'),
        ('functioning', 'Fonctionnement'),
        ('transport_communication', 'Transport et communication'),
        ('investment', 'Investissement'),
        ('rehabilitation', 'Réhabilitation'),
        ('social_assistance', 'Assistance Sociale'),
    ]
    DIRECTION_CHOICES = [
        ('in', 'Income'),
        ('out', 'Expense'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='CDF')
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES, default='in')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES, default='offering')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='financial_transactions')
    category = models.ForeignKey(FinancialCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='transactions')
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='transactions')
    donor_name = models.CharField(max_length=150, blank=True, null=True)
    donor_email = models.EmailField(blank=True, null=True)
    recipient_name = models.CharField(max_length=150, blank=True, null=True)
    recipient_email = models.EmailField(blank=True, null=True)
    recipient_phone = models.CharField(max_length=30, blank=True, null=True)
    payment_method = models.CharField(max_length=40, blank=True, null=True)
    reference_number = models.CharField(max_length=80, blank=True, null=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='cashier_transactions')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_transactions')
    document_number = models.CharField(max_length=32, unique=True, blank=True, null=True)
    receipt_code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    receipt_pdf = models.FileField(upload_to='receipts/', blank=True, null=True)
    receipt_sent_at = models.DateTimeField(blank=True, null=True)
    proof_image = models.ImageField(upload_to='expense_proofs/', blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    image = models.ImageField(upload_to='announcement_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventLogisticsConsumption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='logistics_consumptions')
    item = models.ForeignKey('LogisticsItem', on_delete=models.PROTECT, related_name='event_consumptions')
    quantity_used = models.PositiveIntegerField(default=0)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_event_logistics_consumptions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('event', 'item'),)


class BaptismEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='baptism_event')
    executors = models.JSONField(blank=True, null=True, default=list)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_baptism_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaptismCandidate(models.Model):
    baptism_event = models.ForeignKey(BaptismEvent, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=120)
    post_name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    place_of_birth = models.CharField(max_length=150)
    birth_date = models.DateField()
    passport_photo = models.ImageField(upload_to='baptism_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EvangelismActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('field', 'Descente sur terrain'),
        ('prayer', 'Réunion de prière'),
        ('other', 'Autre'),
    ]
    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='field')
    custom_activity_type = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    moderator = models.CharField(max_length=150, blank=True, null=True)
    published_event = models.OneToOneField(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='evangelism_activity')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_evangelism_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TrainingEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    trainer = models.CharField(max_length=150)
    lesson = models.CharField(max_length=200)
    published_event = models.OneToOneField(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='training_event')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_training_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MarriageRecord(models.Model):
    groom = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='marriages_as_groom', blank=True, null=True)
    bride = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='marriages_as_bride', blank=True, null=True)
    groom_full_name = models.CharField(max_length=200, blank=True, null=True)
    bride_full_name = models.CharField(max_length=200, blank=True, null=True)

    groom_birth_date = models.DateField(blank=True, null=True)
    groom_birth_place = models.CharField(max_length=200, blank=True, null=True)
    groom_nationality = models.CharField(max_length=100, blank=True, null=True)
    groom_passport_photo = models.ImageField(upload_to='marriage_photos/', blank=True, null=True)

    bride_birth_date = models.DateField(blank=True, null=True)
    bride_birth_place = models.CharField(max_length=200, blank=True, null=True)
    bride_nationality = models.CharField(max_length=100, blank=True, null=True)
    bride_passport_photo = models.ImageField(upload_to='marriage_photos/', blank=True, null=True)

    godfather_full_name = models.CharField(max_length=200, blank=True, null=True)
    godfather_nationality = models.CharField(max_length=100, blank=True, null=True)
    godfather_passport_photo = models.ImageField(upload_to='marriage_photos/', blank=True, null=True)

    godmother_full_name = models.CharField(max_length=200, blank=True, null=True)
    godmother_nationality = models.CharField(max_length=100, blank=True, null=True)
    godmother_passport_photo = models.ImageField(upload_to='marriage_photos/', blank=True, null=True)

    planned_date = models.DateField()
    planned_time = models.TimeField()
    location = models.CharField(max_length=200)
    dowry_paid = models.BooleanField(default=False)
    civil_verified = models.BooleanField(default=False)
    prenuptial_tests = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    published_event = models.OneToOneField(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='marriage_record')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_marriage_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AnnouncementLike(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('announcement', 'user')


class AnnouncementComment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='announcement_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class AnnouncementCommentLike(models.Model):
    comment = models.ForeignKey(AnnouncementComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')


class AnnouncementDeck(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='announcement_decks')
    title = models.CharField(max_length=200)
    header_text = models.TextField(blank=True, null=True)
    theme_text = models.TextField(blank=True, null=True)
    pptx_file = models.FileField(upload_to='announcement_decks/', blank=True, null=True)
    generated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_announcement_decks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AnnouncementDeckItem(models.Model):
    deck = models.ForeignKey(AnnouncementDeck, on_delete=models.CASCADE, related_name='items')
    order = models.PositiveIntegerField(default=1)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('sermon', 'Sermon'),
        ('official', 'Official Document'),
        ('report', 'Report'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ApprovalRequest(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    model = models.CharField(max_length=100)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    target_object_id = models.CharField(max_length=64, blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_requests')
    decided_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='decided_approval_requests')
    decided_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LogisticsItem(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('needs_repair', 'Needs Repair'),
        ('damaged', 'Damaged'),
    ]

    CURRENCY_CHOICES = [
        ('CDF', 'CDF'),
        ('USD', 'USD'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    asset_tag = models.CharField(max_length=60, blank=True, null=True, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=30, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    location = models.CharField(max_length=120, blank=True, null=True)
    acquired_date = models.DateField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    purchase_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='CDF')
    supplier = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            qty = int(self.quantity or 0)
        except (TypeError, ValueError):
            qty = 0

        if self.unit_price is not None and qty > 0:
            try:
                self.purchase_price = (Decimal(str(self.unit_price)) * Decimal(qty)).quantize(Decimal('0.01'))
            except (InvalidOperation, TypeError, ValueError):
                pass
        else:
            self.purchase_price = None

        super().save(*args, **kwargs)
        if (not self.asset_tag) and self.pk:
            name = str(self.name or '').strip()
            category = str(self.category or '').strip()

            name_initial = (next((ch for ch in name if ch.isalnum()), '') or 'X').upper()
            category_initial = (next((ch for ch in category if ch.isalnum()), '') or 'X').upper()

            self.asset_tag = f"CDP-LOG-{name_initial}{category_initial}-{self.pk:06d}"
            super().save(update_fields=['asset_tag'])


class LogisticsCategory(models.Model):
    """Catégories dynamiques pour les articles logistiques"""
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie logistique"
        verbose_name_plural = "Catégories logistiques"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name.lower().replace(' ', '_')
        super().save(*args, **kwargs)


class LogisticsCondition(models.Model):
    """États/conditions dynamiques pour les articles logistiques"""
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    display_color = models.CharField(max_length=20, default='secondary', help_text="Couleur du badge (success, warning, danger, info, secondary)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "État logistique"
        verbose_name_plural = "États logistiques"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name.lower().replace(' ', '_')
        super().save(*args, **kwargs)


class AuditLogEntry(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    actor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReportCertificate(models.Model):
    REPORT_TYPE_CHOICES = [
        ('activity', 'Activity Report'),
        ('compiled', 'Compiled Report'),
        ('programme', 'Programme PDF'),
    ]

    code = models.CharField(max_length=40, unique=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    payload = models.JSONField(blank=True, null=True)
    pdf_sha256 = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='report_certificates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChurchBiography(models.Model):
    """Modèle pour gérer la biographie de l'église"""
    title = models.CharField(max_length=200, default="Biographie de l'église")
    content = models.TextField(help_text="Contenu de la biographie de l'église")
    # Champs de contact
    address = models.TextField(blank=True, null=True, help_text="Adresse complète de l'église")
    phone = models.CharField(max_length=50, blank=True, null=True, help_text="Numéro de téléphone principal")
    email = models.EmailField(blank=True, null=True, help_text="Email de contact")
    facebook_url = models.URLField(blank=True, null=True, help_text="Lien Facebook")
    youtube_url = models.URLField(blank=True, null=True, help_text="Lien YouTube")
    instagram_url = models.URLField(blank=True, null=True, help_text="Lien Instagram")
    service_times = models.JSONField(blank=True, null=True, default=list, help_text="Horaires des cultes (JSON)")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='biographies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Biographie de l'église"
        verbose_name_plural = "Biographies de l'église"

    def __str__(self):
        return self.title


class ChurchConsistory(models.Model):
    """Modèle pour gérer les informations du consistoire"""
    title = models.CharField(max_length=200, default="Consistoire de l'église")
    content = models.TextField(help_text="Contenu des informations du consistoire")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='consistories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consistoire de l'église"
        verbose_name_plural = "Consistoires de l'église"

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Modèle pour stocker les messages envoyés via le formulaire de contact"""
    SUBJECT_CHOICES = [
        ('general', 'Demande générale'),
        ('prayer', 'Demande de prière'),
        ('visit', 'Planifier une visite'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('in_progress', 'En cours'),
        ('answered', 'Répondu'),
        ('archived', 'Archivé'),
    ]
    
    name = models.CharField(max_length=150, help_text="Nom complet de l'expéditeur")
    email = models.EmailField(help_text="Email de l'expéditeur")
    phone = models.CharField(max_length=30, blank=True, null=True, help_text="Téléphone de l'expéditeur")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general', help_text="Sujet du message")
    message = models.TextField(help_text="Contenu du message")
    
    # Statut et suivi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', help_text="Statut du message")
    notes = models.TextField(blank=True, null=True, help_text="Notes internes pour l'administration")
    answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='answered_contacts')
    answered_at = models.DateTimeField(blank=True, null=True)
    
    # Métadonnées
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="Adresse IP de l'expéditeur")
    user_agent = models.TextField(blank=True, null=True, help_text="User agent du navigateur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.get_status_display()})"


class ChurchSettings(models.Model):
    """Modèle pour stocker les paramètres globaux de l'application"""
    
    # Informations générales
    church_name = models.CharField(max_length=200, default="Consolation et Paix Divine", help_text="Nom de l'église")
    church_slogan = models.CharField(max_length=300, blank=True, null=True, help_text="Slogan de l'église")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, help_text="Logo de l'application")
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True, help_text="Favicon de l'application")
    
    # Adresse
    address = models.TextField(blank=True, null=True, help_text="Adresse complète")
    city = models.CharField(max_length=100, default="Kinshasa", help_text="Ville")
    country = models.CharField(max_length=100, default="République Démocratique du Congo", help_text="Pays")
    
    # Contacts
    phone_primary = models.CharField(max_length=30, blank=True, null=True, help_text="Téléphone principal")
    phone_secondary = models.CharField(max_length=30, blank=True, null=True, help_text="Téléphone secondaire")
    email_primary = models.EmailField(blank=True, null=True, help_text="Email principal")
    email_secondary = models.EmailField(blank=True, null=True, help_text="Email secondaire")
    
    # Horaires de bureau
    office_hours_weekdays = models.CharField(max_length=100, blank=True, null=True, help_text="Horaires jours de semaine")
    office_hours_saturday = models.CharField(max_length=100, blank=True, null=True, help_text="Horaires samedi")
    office_hours_sunday = models.CharField(max_length=100, blank=True, null=True, help_text="Horaires dimanche")
    
    # Réseaux sociaux
    facebook_url = models.URLField(blank=True, null=True, help_text="URL Facebook")
    youtube_url = models.URLField(blank=True, null=True, help_text="URL YouTube")
    instagram_url = models.URLField(blank=True, null=True, help_text="URL Instagram")
    twitter_url = models.URLField(blank=True, null=True, help_text="URL Twitter/X")
    whatsapp_number = models.CharField(max_length=30, blank=True, null=True, help_text="Numéro WhatsApp")
    telegram_url = models.URLField(blank=True, null=True, help_text="URL Telegram")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paramètre de l'église"
        verbose_name_plural = "Paramètres de l'église"
    
    def __str__(self):
        return self.church_name
    
    def save(self, *args, **kwargs):
        # Empêcher la création de plusieurs instances - Pattern Singleton
        if not self.pk and ChurchSettings.objects.exists():
            # Mettre à jour l'instance existante au lieu d'en créer une nouvelle
            existing = ChurchSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Récupérer ou créer les paramètres"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
