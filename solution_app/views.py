from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from .models import UserCalendar

# Create your views here.
def homePage(request):
    return render(request, 'solution_app/homepage.html')

class GoogleCalendarInitView(View):
    """View to initiate OAuth flow for Google Calendar integration"""

    def get(self, request):
        """Handle GET requests and redirect user to Google OAuth consent"""

        # Create a Flow instance with client secrets, scopes, and redirect URI
        flow = Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'], # read/write
            redirect_uri='/rest/v1/calendar/redirect/'
        )

        # Generate the authorisation URL
        authorisation_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        # Store the state in the session for later verification
        request.session['oauth_state'] = state

        # Redirect user to authorisation URL
        return redirect(authorisation_url)
    # end get() function
# end class GoogleCalendarInitView

class GoogleCalendarRedirectView(View):
    """View to handle redirect request from Google OAuth consent screen"""

    def get(self, request):
        """
        Handle GET requests and exchange the authorisation code
        for an access token
        """

        # Retrieve the stored state from the session
        state = request.session.get('oauth_state')

        # Create a Flow instance with client secrets, scopes, state,
        # and redirect URI
        flow = Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'], # read/write
            state=state,
            redirect_uri='/rest/v1/calendar/redirect/'
        )

        # Exchange authorisation code for credentials
        flow.fetch_token(
            authorization_response=request.build_absolute_uri(),
        )

        # Get credentials
        credentials = flow.credentials

        # Save the credentials to the user's UserCalendar model
        user_calendar, _ = UserCalendar.objects.get_or_create(user=request.user)
        user_calendar.accessToken = credentials.token
        user_calendar.refreshToken = credentials.refresh_token
        user_calendar.tokenExpiry = credentials.expiry
        user_calendar.save()

        # Create a service instance for the Google Calendar API
        service = build('calendar', 'v3', credentials=credentials)

        # Retrieve the list of events from the user's calendar
        events_result = service.events().list(calendarId='primary', 
                                              maxResults=10).execute()
        events = events_result.get('items', [])

        for event in events:
            pass

        return HttpResponse("Events retrieved successfully!")
    # end get() function
# end class GoogleCalendarRedirectView