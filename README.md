# Spotify playing README

A really easy way to display your spotify listening status on READMEs and Websites too!

## Demo

Here's the embed from the site.

[![Spotify playing](http://spotify.aio-api.ml/spotify?id=qy9jhr85so9g8pr6zz7aizc6x&theme=wavy&image=true&bars_when_not_listening=true)](https://open.spotify.com/user/qy9jhr85so9g8pr6zz7aizc6x)

#### Customized card, with theming

[![Spotify playing](http://spotify.aio-api.ml/spotify?id=qy9jhr85so9g8pr6zz7aizc6x&theme=wavy&image=true&bars_when_not_listening=true&bg_color=black&title_color=cyan&text_color=cyan)](https://open.spotify.com/user/qy9jhr85so9g8pr6zz7aizc6x)

## Security notice

**NOTE**: As a security notice, We declare that, we're not storing the sensitive tokens, We just store the 
access tokens securely, used for generating temporary refresh tokens, and getting just the status data, with 
only read permissions and scopes. You can check it in the configuration file for the scopes.

## URL Parameters

- `id`: Your spotify ID
- `theme`: The card theme
- `image`: If cover image to be included
- `eq_bar_theme`: The theme for the EQ bar
- `color_theme`: The color theme for the Card
- `bars_when_not_listening`: If bars should be shown when not listening
- `bg_color`: The BG color for the card
- `title_color`: The title color for the card
- `text_color`: The text color for the card
- `hide_status`: If the status for song should be shown.

## Setting up the development environment

#### Install the dependencies

The project uses pipenv for dependencies. Here's how to install the dependencies.

```sh
pipenv sync -d
```

#### Setting up spotify

- Go to the developer panel at spotify. [Panel URL](https://developer.spotify.com)
- Make an APP, Specify the name, and description.
- Add `http://localhost:5000/callback` to the URLs
- Take a note of the Client ID, and Client Secret for setting up `.env`

#### Setting up Firebase

- Go to the firebase panel.
- Make a new project, and setup as a Web SDK and enable it.
- Go to Settings, and the web apps section, and copy the config, and keep a note.
- Then go to the `Services account` tab, then the `Database secrets`, select the Database we're 
  using and copy the API.
- Copy the domain from Realtime Database section in left, after initializing it.

#### Setting up .env

Configure the environmental variables by renaming the `.env.example` file to `.env` with the respective 
values for it.

Here's the info about the variables

- `BASE_URL`: This is the basic URL for local dev, set it to `localhost:5000`
- `SPOTIFY_CLIENT_ID`: This is the spotify client ID. 
- `SPOTIFY_SECRET_ID`: This is the Spotify Secret.
- `FB_API_KEY`: This is the API key for firebase, from Database secrets.
- `FB_DOMAIN`: This is the domain from `Realtime Database` section.
- `FB_PROJECT_ID`: This is the Project ID from normal firebase config.
- `FB_STORAGE_BUCKET`: The storage bucket from the normal firebase config.
- `FB_MESSAGING_ID`: The messaging ID from normal firebase config.
- `FB_DATABASE_URL`: The database URL from firebase config.

**Once done, Run the server using `pipenv run start`! It should boot up at `localhost:5000`! Enjoy!**

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
  - [x] Allow customizing Background and font color ( Will be redeveloped, with all security issues fixed )
  - [x] Marquee show
  - [x] Display bars when not listening.
  - [x] Allow linking to your profile along with the link.
  - [x] Color Theme
  - [x] Abiltiy to Hide status
  - [x] HTML Image tag generation
  - [x] Add same color to either of the text / title, if either of them is left empty, so the color pallet is fine.

## 🤝 Contributing

Contributions, issues and feature requests are welcome. After cloning & setting up project locally, you can just submit 
a PR to this repo and it will be deployed once it's accepted.

⚠️ It’s good to have descriptive commit messages, or PR titles so that other contributors can understand about your 
commit or the PR Created. Read [conventional commits](https://www.conventionalcommits.org/en/v1.0.0-beta.3/) before 
making the commit message.

## 💬 Get in touch

If you have various suggestions, questions or want to discuss things wit our community, Join our discord server!

[![Discord](https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield)](https://discord.gg/cSC5ZZwYGQ)

## Show your support

We love people's support in growing and improving. Be sure to leave a ⭐️ if you like the project and 
also be sure to contribute, if you're interested!

## License

- [GPL V3](https://github.com/janaSunrise/spotify-playing-readme/blob/main/LICENSE)

**Inspired by [Novatorem](https://github.com/novatorem)**

<div align="center">
  Made by Sunrit Jana with ❤️
</div>
