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
            <input type="password" class="form-control" id="password" v-model="password" required placeholder="Password" @focus="passwordTouched = true" @blur="handlePasswordBlur">
            <div v-if="passwordTouched && isPasswordBlank" class="invalid-feedback d-block">Password is required.</div>
          </div>
          <div class="mb-4 form-check">
            <input type="checkbox" class="form-check-input" id="remember-me" v-model="rememberMe">
            <label class="form-check-label" for="remember-me">Remember me</label>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary" :disabled="emailError || isPasswordBlank || isEmailBlank">Login</button>
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
      passwordTouched: false,
      loginErrorMessage: 'Invalid username and/or password.',
      emailErrorMessage: 'Please enter a valid email address.'
    };
  },
  computed: {
    isPasswordBlank() {
      return this.password.trim() === '';
    },
    isEmailBlank() {
      return this.email.trim() === '';
    }
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
            
            // Update user_level and user_id in the Vuex store
            this.$store.commit('SET_AUTHENTICATED', true);
            this.$store.commit('SET_USER_LEVEL', data.data.user_level);
            this.$store.commit('SET_USER_ID', data.data.user_id);

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

      if (this.email.trim() === '') {
        // Handle empty email field
        this.emailError = true;
        this.emailErrorMessage = 'Email address is required.';
      } else if (!pattern.test(this.email)) {
        // Handle invalid email format
        this.emailError = true;
        this.emailErrorMessage = 'Please enter a valid email address.';
      } else {
        // Email is valid
        this.emailError = false;
        this.emailErrorMessage = '';
      }
    },
    handlePasswordBlur() {
      if (this.password.trim() === '') {
        this.passwordTouched = true;
      }
    },
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
