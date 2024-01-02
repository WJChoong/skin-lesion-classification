import { createRouter, createWebHashHistory } from "vue-router";
import ImageUploader from "../components/ImageUploader.vue";
import LoginPage from "../components/LoginPage";
import ImageTable from "../components/ImageTable";
import ResetPassword from "../components/ResetPassword";
import ManageUser from "../components/ManageUser";

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
  {
    path: "/resetpass",
    name: "ResetPassword",
    component: ResetPassword,
  },
  {
    path: "/manageuser",
    name: "ManageUser",
    component: ManageUser,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
