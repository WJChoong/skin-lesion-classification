<template>
  <div class="container mt-3 mb-3">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card my-5">
          <div class="card-header text-center">Reset Password</div>
          <div class="card-body">
            <form @submit.prevent="submitEmail">
              <div class="form-group">
                <label for="emailInput">Email address</label>
                <input type="email" class="form-control mt-3 mb-3" id="emailInput" placeholder="Enter email" v-model="email" required>
                <small v-show="emailError" class="text-danger">{{ emailError }}</small>
              </div>
              <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ loading ? 'Processing...' : 'Reset Password' }}
              </button>
            </form>
            <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
              {{ errorMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  data() {
    return {
      email: '',
      emailError: '',
      errorMessage: '',
      successMessage: '',
      loading: false
    };
  },
  methods: {
    validateEmail(email) {
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    submitEmail() {
      this.emailError = '';
      this.errorMessage = '';
      this.successMessage = '';
      this.loading = true;

      if (!this.validateEmail(this.email)) {
        this.emailError = 'Please enter a valid email address.';
        this.loading = false;
        return;
      }

      const apiUrl = 'http://localhost:4040/auth/reset/';
      axios.post(apiUrl, { email: this.email })
        .then(response => {
          this.loading = false;
          this.successMessage = response.data.message;
          setTimeout(() => {
            this.$router.push('/');
          }, 3000);
        })
        .catch(error => {
          this.loading = false;
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = 'An error occurred while attempting to reset the password.';
          }
        });
    }
  }
}
</script>