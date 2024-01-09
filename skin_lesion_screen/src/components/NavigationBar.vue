<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <router-link to="/" class="navbar-brand ml-3">Upload Image</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/profile" class="nav-link">Profile</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated && user_level === '1'">
          <router-link to="/user" class="nav-link">Manage User</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/image" class="nav-link">Manage Image</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/" class="nav-link" @click="logout">Logout</router-link>
        </li>
        <li class="nav-item text-white" v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { mapState } from 'vuex';
import LoginPage from '../components/LoginPage.vue'

export default {
  name: 'NavigationBar',
  data() {
    return {
      auth: false,
    };
  },
  components: {
    LoginPage
  },
  computed: {
    ...mapState({
      isAuthenticated: state => state.isAuthenticated,
      user_level: state => state.user_level
    }),
  },
  methods: {
    logout() {
      this.$store.commit('clearUserData');
    }
  }
};
</script>
