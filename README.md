# kadro_to_google
## Problem
Cinemacity uses "kadromierz" as site where all employers are informed about their shifts and most important info. As app works perfectly with push notifications, the shift viewer does not work well. It requires you to be always connected to web and works very slowly due to ongoing synchronization. 
![Kadromierz view](/docs/fot1.png)
## Solution
I decided to create service which I can run on home raspbery and every hour It will create google calendar events for every employer.
![GCalendar view](/docs/fot2.png)
## Dependeccies
### Needed python modules:
- urllib3
- google-api-python-client 
- google-auth-httplib2 
- google-auth-oauthlib
### Additional files
- **token** - *token to access google calendar*
- **savings.json** - *this file contains setting and pass to kadrometr*