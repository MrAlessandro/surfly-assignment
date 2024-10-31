import { createRouter, createWebHistory } from "vue-router";
import Identification from "../views/Identification.vue"; // Adjust the path as needed
import Drawer from "../views/Drawer.vue"; // Adjust the path as needed

const routes = [
  {
    path: "/",
    name: "Identification",
    component: Identification,
  },
  {
    path: "/drawer",
    name: "Drawer",
    component: Drawer,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for username in localStorage
router.beforeEach((to, from, next) => {
  const username = localStorage.getItem("username");
  if (!username && to.path !== "/") {
    // Redirect to the user form if no username is found and the route is not the form page
    next({ path: "/" });
  } else if (username && to.path === "/") {
    // Redirect to the canvas page if username exists and the route is the form page
    next({ path: "/drawer" });
  } else {
    next(); // Proceed to the route
  }
});

export default router;
