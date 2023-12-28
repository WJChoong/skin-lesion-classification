import { createRouter, createWebHashHistory } from "vue-router";
import ImageUploader from "../components/ImageUploader.vue";
import LoginPage from "../components/LoginPage";
import ImageTable from "../components/ImageTable";

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
  {
    path: "/verify",
    name: "ImageTable",
    component: ImageTable,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
