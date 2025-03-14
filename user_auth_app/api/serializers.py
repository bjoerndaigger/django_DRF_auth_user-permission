from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

# Importiert das ModelSerializer von DRF (Django REST Framework),
# das die automatische Serialisierung eines Django-Modells ermöglicht.


class RegistrationSerializer(serializers.ModelSerializer):
    # Ein zusätzliches Feld für die Passwort-Wiederholung,
    # das nur beim Schreiben verwendet wird (nicht in API-Ausgaben erscheint).
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        # Verknüpft den Serializer mit dem User-Modell.
        model = User
        # Gibt an, welche Felder in der Serialisierung enthalten sein sollen.
        fields = ['username', 'email', 'password', 'repeated_password']
        # Stellt sicher, dass das Passwort nur geschrieben, aber nie zurückgegeben wird.
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # Überschreibt die save()-Methode, um eigene Logik beim Speichern des Nutzers hinzuzufügen.
    def save(self):
        # Holt das Passwort und das wiederholte Passwort aus den validierten Daten.
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        # Prüft, ob beide Passwörter übereinstimmen.
        if pw != repeated_pw:
            # Wenn nicht, wird eine Validierungsfehlermeldung ausgelöst.
            raise serializers.ValidationError(
                {'error': 'passwords dont match'})

        # Erstellt ein neues User-Objekt mit den eingegebenen Daten (ohne Passwort).
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        # Setzt das Passwort sicher (hashed, nicht im Klartext gespeichert).
        account.set_password(pw)
        # Speichert den User in der Datenbank.
        account.save()
        # Gibt den erstellten User zurück.
        return account
