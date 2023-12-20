import { createRouter, createWebHashHistory } from "vue-router";
import ImageUploader from "../components/ImageUploader.vue";
import LoginPage from "../components/LoginPage";

const routes = [
  {
    path: "/",
    name: "ImageUploader",
    component: ImageUploader,
  },
  {
    path: "/login",
    name: "LoginPage",
    component: LoginPage,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
