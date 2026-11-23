# aevai build: official argilla-server image + this fork's frontend + the server files we patched.
# Build context = repo root:  docker build -f aevai/Dockerfile .
ARG ARGILLA_VERSION=v2.8.0

# full image: native deps (deasync) need python3 + a compiler
FROM node:20 AS frontend
# same layout as the repo: the frontend imports ../docs/_source/_common (keyboard shortcuts help)
WORKDIR /repo/argilla-frontend
COPY argilla-frontend/package.json argilla-frontend/package-lock.json ./
# upstream lock file is out of sync with package.json, so `npm ci` fails; upstream CI uses `npm install` too
RUN npm install --no-audit --no-fund
COPY docs/_source/_common /repo/docs/_source/_common
COPY argilla-frontend/ ./
RUN BASE_URL="@@baseUrl@@" DIST_FOLDER=./dist npm run build

FROM argilla/argilla-server:${ARGILLA_VERSION}
ARG PKG=/opt/venv/lib/python3.13/site-packages/argilla_server
RUN rm -rf $PKG/static
COPY --chown=argilla:argilla --from=frontend /repo/argilla-frontend/dist $PKG/static
# patched server files (keep this list short; each one must still match the base image version)
COPY --chown=argilla:argilla argilla-server/src/argilla_server/search_engine/commons.py $PKG/search_engine/commons.py
