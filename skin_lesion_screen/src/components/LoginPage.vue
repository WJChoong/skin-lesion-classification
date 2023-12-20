<template>
  <div class="vh-100 d-flex align-items-center justify-content-center custom-dark-bg">
    <div class="card text-white bg-secondary mb-3 w-100" style="max-width: 400px;">
      <div class="card-header text-center">Login</div>
      <div class="card-body">
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="username" class="form-label">Email address</label>
            <input type="email" class="form-control" id="username" v-model="username" required placeholder="Enter email">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" required placeholder="Password">
          </div>
          <div class="mb-4 form-check">
            <input type="checkbox" class="form-check-input" id="remember-me">
            <label class="form-check-label" for="remember-me">Remember me</label>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
        </form>
        <div class="mt-4 text-center">
          <a href="#" class="text-light">Forgot password?</a>
          <span class="text-white mx-2">|</span>
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
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
        if (this.email === 'hello123@gmail.com' && this.password === 'hello123') {
            console.log('Login success');

            // Redirect to the home page
            this.$router.push({ name: 'ImageUploader' });
        } else {
            console.log('Login failed');
        }
    }
  }
};
</script>

<style scoped>
.custom-dark-bg {
  background-color: #343a40; /* A lighter shade of dark */
}
</style>
