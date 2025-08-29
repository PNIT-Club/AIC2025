# How to boot up UI
- Open the first folder (AI-challenge-UI)
- Either use live server extension (served at localhost, port **5500**, by default), or set up a web server (Apache or Nginx)
- Search

# How to boot up backend
- Open the second folder (OpenAiServer) in Intellij
- Copy back all the keyframe images into the `%PROJECT_ROOT%/src/res/images` (L21_V001, L21_V002, etc)
- Download all the dependencies
- Run (Server served at localhost, port **5000**)
###### Note: Server only has 1 endpoint, at `https://localhost:5000/search?q=[QUERY]&searchType=[SEARCH_TYPE]`, the `SEARCH_TYPE` field isn't implemented for now.

