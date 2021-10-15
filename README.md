# Twitch_Farm
Join Twitch Chats, farm Activity Points in several bots and participate in Raffles!

## How to use
`git clone https://github.com/le3ch-tech/twitch_farm.git`

- Copy `example.json` and rename it to `config.json`
- Replace values with own preferences

### Creating a token
- Goto https://dev.twitch.tv/ and connect "Twitch Developer" with your Twitch Account
- Now, visit https://dev.twitch.tv/console/apps and create a new application
- Add `https://localhost` as Redirect URI. If that doesn't work for whatever reason, add `http://localhost` as well and Twitch will allow you to safe both
- Visit `https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=<YOUR_CLIENT_ID>&redirect_uri=http://localhost&scope=chat:read+chat:edit+whispers:read+whispers:edit&state=frontend|dkZud25INzhpWFEzWVFxY3lpQ0tMZz09&force_verify=true`, replacing `<YOUR_CLIENT_ID>` with the Client ID of the application you just created
- After accepting the connection with Twitch you will redirected to a localhost. The connection will fail, but the URL in your browser will include the token you need for the script.


### OUTDATED
