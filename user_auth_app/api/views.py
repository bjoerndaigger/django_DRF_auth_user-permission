from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    # Weil in den globalen Einstellungen 'DEFAULT_PERMISSION_CLASSES' auf 'IsAuthenticated' gesetzt ist,
    # wird hier 'AllowAny' gesetzt, damit sich jeder Nutzer registrieren kann, ohne angemeldet zu sein.
    permission_classes = [AllowAny]

    # Die POST-Methode wird aufgerufen, wenn eine Anfrage an diesen Endpunkt geschickt wird.
    def post(self, request):
        # Erstelle einen Serializer, um die vom Client gesendeten Daten zu validieren
        serializer = RegistrationSerializer(data=request.data)

        # Initialisiere ein leeres Daten-Dictionary, das später die Antwort enthalten wird.
        data = {}

        # Wenn die übergebenen Daten validiert sind (alle Anforderungen stimmen),
        # wird der Benutzer gespeichert und ein Authentifizierungstoken erstellt.
        if serializer.is_valid():
            # Speichert den neuen Benutzer und gibt das Benutzerobjekt zurück
            saved_account = serializer.save()

            # Erstellt ein Authentifizierungstoken für den neu registrierten Benutzer.
            # `get_or_create` sucht nach einem bestehenden Token für den Benutzer.
            # Wenn kein Token vorhanden ist, wird ein neues Token erstellt.
            # `created` ist ein Boolean-Wert, der angibt, ob das Token neu erstellt wurde (True) oder bereits existiert (False).
            token, created = Token.objects.get_or_create(user=saved_account)

            # Die Antwort-Daten (das Token und die Benutzerdaten) werden hier gesetzt.
            data = {
                'token': token.key,  # Der Token wird zur Authentifizierung im Header verwendet
                'username': saved_account.username,  # Der Benutzername des neu erstellten Kontos
                'email': saved_account.email  # Die E-Mail-Adresse des Benutzers
            }
        else:
            # Falls die Daten ungültig sind, wird das Fehler-Objekt des Serializers zurückgegeben
            data = serializer.errors

        # Gibt die Antwort zurück, die entweder das Token und die Benutzerdaten oder Fehler enthält.
        return Response(data)


# CustomLoginView ist eine benutzerdefinierte View, die von ObtainAuthToken erbt,
# um die Standard-Login-Logik zu erweitern und anzupassen.
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    # POST-Methode zum Verarbeiten der Anmeldeinformationen des Benutzers.
    def post(self, request):
        # Erstelle einen Serializer (der standardmäßig von `ObtainAuthToken` bereitgestellt wird), um die vom Client gesendeten Daten zu validieren.
        serializer = self.serializer_class(data=request.data)

        # Initialisiere ein leeres Dictionary, das später die Antwort-Daten enthalten wird.
        data = {}

        if serializer.is_valid():
            # Extrahiere den Benutzer aus den validierten Daten des Serializers.
            user = serializer.validated_data['user']

            # Wenn der Benutzer existiert, versuche, ein Authentifizierungstoken zu erstellen.
            # 'get_or_create' sorgt dafür, dass nur ein Token für diesen Benutzer existiert.
            token, created = Token.objects.get_or_create(user=user)

            # Erstelle das Antwort-Daten-Dictionary mit dem Token, Benutzernamen und der E-Mail-Adresse.
            data = {
                'token': token.key,  # Das generierte Token, das zur Authentifizierung verwendet wird.
                'username': user.username,  # Der Benutzername des authentifizierten Benutzers.
                'email': user.email  # Die E-Mail-Adresse des Benutzers.
            }
        else:
            # Falls die Anmeldeinformationen ungültig sind, gebe die Fehler des Serializers zurück.
            data = serializer.errors

        # Gibt die Antwort zurück, die entweder das Token und Benutzerdaten oder Fehler enthält.
        return Response(data)

