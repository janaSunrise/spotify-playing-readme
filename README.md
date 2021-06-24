# Spotify playing README

A really easy way to display your spotify listening status on READMEs and Websites too!

## Demo

Here's the embed from the site.

[![Spotify playing](http://spotify.aio-api.ml/spotify?id=qy9jhr85so9g8pr6zz7aizc6x&theme=wavy&image=true&bars_when_not_listening=true)](https://open.spotify.com/user/qy9jhr85so9g8pr6zz7aizc6x)

#### Customized card, with theming

[![Spotify playing](http://spotify.aio-api.ml/spotify?id=qy9jhr85so9g8pr6zz7aizc6x&theme=wavy&image=true&bars_when_not_listening=true&bg_color=black&title_color=cyan&text_color=cyan)](https://open.spotify.com/user/qy9jhr85so9g8pr6zz7aizc6x)

## Security notice

As a security notice, We declare that, we're not storing the sensitive tokens, We just store the 
access tokens securely, used for generating temporary refresh tokens, and getting just the status data, with 
only read permissions and scopes. You can check it in the configuration file for the scopes.

## URL Parameters

- `id`: Your spotify ID
- `theme`: The card theme
- `image`: If cover image to be included
- `color_theme`: The color theme for the Card
- `bars_when_not_listening`: If bars should be shown when not listening
- `bg_color`: The BG color for the card
- `title_color`: The title color for the card
- `text_color`: The text color for the card
- `hide_status`: If the status for song should be shown.

**NOTE**: You can generate the card easily by visiting the panel. Check the repo description link for it.

## Setting up the development environment

#### Install the dependencies

The project uses pipenv for dependencies. Here's how to install the dependencies.

```sh
pipenv sync -d
```

#### Setting up Spotify

- Go to the developer panel at spotify. [Panel URL](https://developer.spotify.com)
- Make an APP, Specify the name, and description.
- Add `http://localhost:5000/callback` to the URLs for development. Add the respective IP / Domain / Host
  if you're self hosting this App with the path of `/callback` to the end.
- Take a note of the Client ID, and Client Secret for setting up `.env`

#### Setting up Firebase

- Go to the firebase panel.
- Make a new project, and setup as a Web SDK and enable it.
- Go to Settings, and the web apps section, and copy the config, and keep a note.
- Then go to the `Services account` tab, then the `Database secrets`, select the Database we're 
  using and copy the API.
- Copy the domain from Realtime Database section in left, after initializing it.
- Finally, For service accounts, Go to the `Services account` tab. Then download the service
  account credentials and save it. Once done, Open VSCode, Download Base64 Encode extension, 
  if you don't already have it. The Copy and Paste the JSON file contents in the `.env` and 
  Encode it using Base64 after that.

#### Setting up .env

Configure the environmental variables by renaming the `.env.example` file to `.env` with the respective 
values for it.

Here's the info about the variables

- `BASE_URL`: This is the basic URL for getting the Callback URLs and more, set it 
  to `localhost:5000` in development mode.
- `SPOTIFY_CLIENT_ID`: This is the spotify client ID. 
- `SPOTIFY_SECRET_ID`: This is the Spotify Secret.
- `FB_API_KEY`: This is the API key for firebase, from Database secrets.
- `FB_DOMAIN`: This is the domain from `Realtime Database` section.
- `FB_PROJECT_ID`: This is the Project ID from normal firebase config.
- `FB_STORAGE_BUCKET`: The storage bucket from the normal firebase config.
- `FB_MESSAGING_ID`: The messaging ID from normal firebase config.
- `FB_DATABASE_URL`: The database URL from firebase config.
- `FB_SERVICE_ACCOUNT`: The service account credentials obtained from the settings and encoded using base64.

**NOTE**: Use the VSCode Base64 encode extension to encode the contents of the Service Account JSON file.

You can change the port when self hosting / running by adding a `port` parameter to `flask_app`'s `run`
function. You can do so like this `flask_app.run(debug=DEBUG, port=<the-port-you-need>)`

Once done, Run the server using **`pipenv run start`**. It should boot up at `localhost:5000` in development mode, 
or the settings you have provided.

## Deploying your own instance

To deploy your own instance, You need a proper hosting platform to run Python webapps.
You can use Heroku, PythonAnywhere, Your own server or anywhere else.

To self-host your instance, The steps are given above on how to do it. The instructions on
option configuration is also given. It is recommended to run with Debug mode off, and Your 
specific host and port.

You can do so, like this:
- Turn debug off, by toggling the Debug option to `False` in `config.py`
- Change host and port: `flask.run(debug=DEBUG, host="<your-host>", port=<your-port>)` by replacing
  the values given inside the angle brackets.
  
Here is the workflow on setting up:
- Setup Spotify API and note it.
- Setup Firebase for data store and note the API.
- Fill the values as said in `.env`.
- Configure the options as needed.
- Install dependencies using `pipenv`.
- Run using **`pipenv run start`**.
- And, you should be good to go.

**Note**: You can use out self hosted instance already running, or Self host your own like this.

## TODOs Planned

There are several things planned for this project. Here are the TODOs, Kept public for reference,
and transparent-ness.

- [ ] FAQ
  - [ ] How to contribute
  - [ ] How to add a theme
  - [ ] How to work with options
  - [ ] Adding more features
  - [ ] Customization
- [x] Improve the current themes  
- [ ] Add more themes
- [x] Add more customization options
  - [x] Previews when customizing the card
  - [x] Allow customizing Background and font color (Will be redeveloped, with all security issues fixed)
  - [x] Marquee show
  - [x] Display bars when not listening.
  - [x] Allow linking to your profile along with the link.
  - [x] Color Theme
  - [x] Abiltiy to Hide status
  - [x] HTML Image tag generation
  - [x] Add same color to either of the text / title, if either of them is left empty, so the color pallet is fine.

## 🤝 Contributing

Contributions, issues and feature requests are welcome. After cloning & setting up project locally, you can 
just submit a PR to this repo and it will be deployed once it's accepted.

⚠️ It’s good to have descriptive commit messages, or PR titles so that other contributors can understand 
about your commit or the PR Created. Read 
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0-beta.3/) before making the commit message.

## Show your support

We love people's support in growing and improving. Be sure to leave a ⭐️ if you like the project and 
also be sure to contribute, if you're interested!

**Inspired by [Novatorem](https://github.com/novatorem)**

<div align="center">Made by Sunrit Jana with ❤️</div>
