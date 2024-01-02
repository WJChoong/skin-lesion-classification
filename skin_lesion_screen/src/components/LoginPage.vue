<template>
  <div class="vh-100 d-flex align-items-center justify-content-center custom-dark-bg">
    <div class="card text-white bg-secondary mb-3 w-100" style="max-width: 400px;">
      <div class="card-header text-center">Login</div>
      <div class="card-body">
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" v-model="email" required placeholder="Enter email" @input="validateEmail">
            <div v-if="emailError" class="invalid-feedback d-block">{{ emailErrorMessage }}</div>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" required placeholder="Password">
            <div v-if="loginError" class="invalid-feedback d-block">{{ loginErrorMessage }}</div>
          </div>
          <div class="mb-4 form-check">
            <input type="checkbox" class="form-check-input" id="remember-me" v-model="rememberMe">
            <label class="form-check-label" for="remember-me">Remember me</label>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary" :disabled="emailError">Login</button>
          </div>
        </form>
        <div class="mt-4 text-center">
          <router-link to="/resetpass" class="text-light">Forgot password?</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      loginError: false,
      emailError: false,
      loginErrorMessage: 'Invalid username and/or password.',
      emailErrorMessage: 'Please enter a valid email address.'
    };
  },
  methods: {
    async login() {
    if (!this.emailError && this.email && this.password) {
      const requestData = {
        email: this.email,
        password: this.password,
      };

      await fetch('http://localhost:4040/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          console.log('Login success');
          if (this.rememberMe) {
            localStorage.setItem('rememberedEmail', this.email);
          } else {
            localStorage.removeItem('rememberedEmail');
          }
          this.$store.commit('SET_AUTHENTICATED', true);
          // Redirect to the home page
          this.$router.push({ name: 'ImageUploader' });
        } else {
          this.loginError = true;
          this.password = '';
        }
      })
      .catch(error => {
        console.error('Error:', error);
        this.loginError = true;
        this.password = '';
      });
    } else {
      this.loginError = true;
      this.password = '';
    }
  },
    validateEmail() {
      // Simple regex for basic email validation
      const pattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
      this.emailError = !pattern.test(this.email);
    }
  },
  created() {
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail) {
      this.email = rememberedEmail;
      this.rememberMe = true;
    }
  }
};
</script>

<style scoped>
.custom-dark-bg {
  background-color: #343a40; /* A lighter shade of dark */
}

.invalid-feedback {
  color: #e3342f; /* Bootstrap danger color */
}

.d-block {
  display: block;
}
</style>
