<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">Image Uploader</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/profile" class="nav-link">Profile</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/verify" class="nav-link">Verify</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/verify" class="nav-link">Manage User</router-link>
        </li>
        <li class="nav-item" v-else>
          <router-link to="/manageuser" class="nav-link">Manage User</router-link>
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
      auth: false
    };
  },
  components: {
    LoginPage
  },
  methods: {
    receiveMessage(message) {
      console.log('Message received from child:', message);
    }
  },
  computed: {
    ...mapState({
      isAuthenticated: state => state.isAuthenticated
    })
  }
};
</script>
