from rest_framework import generics, permissions, serializers 
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from api.models import Patient, MUser

class UniqueFieldsMixin(serializers.ModelSerializer):
    _unique_fields = []

    def get_fields(self):
        self._unique_fields = []

        fields = super(UniqueFieldsMixin, self).get_fields()
        for field_name, field in fields.items():
            is_unique = any([isinstance(validator, UniqueValidator) for validator in field.validators])

            if is_unique:
                self._unique_fields.append(field_name)
                field.validators = [validator for validator in field.validators if not isinstance(validator, UniqueValidator)]

        return fields

    def _validator_unique_fields(self, validated_data):
        for field_name in self._unique_fields:
            unique_validator = UniqueValidator(self.Meta.model.objects.all())
            unique_validator.set_context(self.fields[field_name])

            try:
                unique_validator(validated_data[field_name])
            except ValidationError as exc:
                raise ValidationError({field_name: exc.detail})

    def create(self, validated_data):
        self._validator_unique_fields(validated_data)
        return super(UniqueFieldsMixin, self).create(validated_data)

    def update(self, instance, validated_data):
        self._validator_unique_fields(validated_data)
        return super(UniqueFieldsMixin, self).update(instance,validated_data)
            

class UserSerializer(UniqueFieldsMixin,serializers.ModelSerializer):

    class Meta:
        model = MUser
        fields = (
            'id',
            'email', 
            'password', 
            'date_of_birth', 
            'first_name', 
            'last_name', 
            'gender'
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('patient_no',)

        
class PatientSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Patient
        fields = (
            'id',
            'patient_no', 
            'patient_type',
            'region',
            'user',
            'slug',
        )
        depth = 1

    def create(self, validated_data):
        
        user_data = validated_data.pop('user')
        
        user = MUser.objects.create_patient(**user_data)
        patient = Patient.objects.create(user=user,**validated_data)
        
        return patient
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        user = instance.user
        user.email = user_data.get(
            'email',
            user.email
        )
        user.password = user_data.get(
            'password',
            user.password
        )
        user.date_of_birth = user_data.get(
            'date_of_birth',
            user.date_of_birth
        )
        user.first_name = user_data.get(
            'first_name',
            user.first_name
        )
        user.last_name = user_data.get(
            'last_name',
            user.last_name
        )
        user.gender = user_data.get(
            'gender',
            user.gender
        )

        instance.patient_no = validated_data.get('patient_no', instance.patient_no)
        instance.patient_type = validated_data.get('patient_type', instance.patient_type)
        instance.region = validated_data.get('region', instance.region)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()

        return instance

    
