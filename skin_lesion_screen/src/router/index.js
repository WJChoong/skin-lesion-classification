import { createRouter, createWebHashHistory } from "vue-router";
import ImageUploader from "../components/ImageUploader.vue";
import LoginPage from "../components/LoginPage";
import ImageTable from "../components/ImageTable";
import ResetPassword from "../components/ResetPassword";
import ManageUser from "../components/ManageUser";
import Profile from "../components/Profile";

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
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/image",
    name: "ImageTable",
    component: ImageTable,
  },
  {
    path: "/resetpass",
    name: "ResetPassword",
    component: ResetPassword,
  },
  {
    path: "/user",
    name: "ManageUser",
    component: ManageUser,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
