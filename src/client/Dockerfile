FROM node:18.12.0-slim

RUN npm install -g @angular/cli

WORKDIR /ng-app

COPY package.json .

RUN npm install

COPY . .

CMD ng analytics off && ng serve --host 0.0.0.0 --port 4200 --disable-host-check

EXPOSE 4200