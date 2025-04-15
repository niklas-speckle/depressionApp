from .models import HealthProfessionalProfile

def is_allowed_to_read(requester, target_patient_profile):
    """Check if the requester has permission to read the target patient's profile."""
    # Check if the requester is the patient themselves
    if requester == target_patient_profile.user:
        return True

    # Check if the requester is a health professional and the target patient is their patient
    if requester.groups.filter(name="Health-Professional").exists():
        health_professional_profile = HealthProfessionalProfile.objects.get(user=requester)
        return health_professional_profile in target_patient_profile.health_professional.all()

    return False