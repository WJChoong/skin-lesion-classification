<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">Image Uploader</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item" v-if="auth.isAuthenticated">
          <a class="nav-link" href="/profile">Profile</a>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <a class="nav-link" href="/verify">Verify</a>
        </li>
        <li class="nav-item" v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
// import { auth } from '../middleware/auth';
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
  }
};
</script>
