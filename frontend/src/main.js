import { createApp } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import App from "./App.vue";
import HomeView from "./views/HomeView.vue";
import DetectView from "./views/DetectView.vue";
import ChatView from "./views/ChatView.vue";
import GameView from "./views/GameView.vue";
import IntelView from "./views/IntelView.vue";
import HelpView from "./views/HelpView.vue";
import AboutView from "./views/AboutView.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/detect", name: "detect", component: DetectView },
    { path: "/chat", name: "chat", component: ChatView },
    { path: "/game", name: "game", component: GameView },
    { path: "/intel", name: "intel", component: IntelView },
    { path: "/help", name: "help", component: HelpView },
    { path: "/about", name: "about", component: AboutView },
  ],
});

createApp(App).use(router).mount("#app");
