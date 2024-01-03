<template>
  <div class="container mt-5">
    <div class="row">
      <!-- User Details Form Section -->
      <div class="col-md-6 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Update User Details</h5>
            <!-- Form elements here -->
            <form @submit.prevent="updateDetails">
              <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" class="form-control" v-model="user.name" :readonly="!editing">
              </div>
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" class="form-control" v-model="user.email" :readonly="!editing">
              </div>
              <div class="form-group">
                <label for="country">Country</label>
                <input type="text" id="country" class="form-control" v-model="user.country" :readonly="!editing">
              </div>
              <span v-if="loading" class="spinner-border mt-3" role="status" aria-hidden="true"></span>

                <div v-if="successMessage" class="alert alert-success mt-3">
                {{ successMessage }}
                </div>
                
                <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
                </div>
              <button v-if="!editing" type="button" class="btn btn-primary mt-3" @click="enableEditing">
                Edit
              </button>
              <div v-if="editing">
                <button type="submit" class="btn btn-success mt-3" style="margin-right: 8px;">
                    Save Changes
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </button>
                <button type="button" class="btn btn-secondary mt-3" @click="cancelEditing">
                    Cancel
                </button>
            </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Change Password Form Section -->
      <div class="col-md-6 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Change Password</h5>
            <!-- Form elements here -->
            <form @submit.prevent="changePassword">
                <div class="form-group">
                    <label for="oldPassword">Old Password</label>
                    <input type="password" id="oldPassword" class="form-control" v-model="password.oldPassword">
                </div>
                <div class="form-group">
                    <label for="newPassword">New Password</label>
                    <input type="password" id="newPassword" class="form-control" v-model="password.newPassword">
                </div>
                <div class="form-group">
                    <label for="confirmNewPassword">Re-enter New Password</label>
                    <input type="password" id="confirmNewPassword" class="form-control" v-model="password.confirmNewPassword">
                </div>
                <button type="submit" class="btn btn-primary mt-3" :disabled="loading">
                    Change Password
                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios'); // Ensure you have axios installed or use a different HTTP client

export default {
  data() {
    return {
    //   user_id: '',
      editing: false,
      loading: false,
      successMessage: '',
      errorMessage: '',
      user: {
        name: '',
        email: '',
        country: ''
      },
      password: {
        oldPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      }
    };
  },
  created() {
    this.user_id = this.$store.state.user_id;
    if (!this.isAuthenticated || !this.user_id){
        this.$router.push({ name: 'LoginPage' });
    }
    this.getUserDetails();
  },
  methods: {
    async getUserDetails() {
      try {
        this.loading = true;
        const response = await axios.get('http://localhost:4040/user/get/user/', {
          params: { id: this.user_id }
        });
        if (response.data.status === 'success') {
          const { name, email, country } = response.data.data;
          this.user.name = name;
          this.user.email = email;
          this.user.country = country;
        } else {
          // Handle any errors, such as user not found
          console.error(response.data.message);
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async updateDetails() {
      this.loading = true;
      try {
        const response = await axios.put('http://localhost:4040/user/update/', {
          id: this.user_id,
          name: this.user.name,
          email: this.user.email,
          country: this.user.country
        });
        // On success
        if (response.data.status === 'success') {
            this.successMessage = 'Operation successful!';
            // Additional success handling
        } else {
            this.errorMessage = 'An error occurred. Please try again.';
            // Additional error handling
        }
      } catch (error) {
        // Handle the error
        console.error('An error occurred:', error);
      }
      this.loading = false;
      this.editing = false;
    },
    async changePassword() {
      this.loading = true;
      try {
        const response = await axios.put('/change-password-api-endpoint', {
          user_id: this.user_id,
          old_password: this.password.oldPassword,
          new_password: this.password.newPassword
        });
        // On success
        if (response.data.status === 'success') {
          // Handle success
        } else {
          // Handle failure
        }
      } catch (error) {
        // Handle the error
        console.error('An error occurred:', error);
      }
      this.loading = false;
    },
    enableEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
    },
  },
  computed: {
    user_id: {
      get() {
        return this.$store.state.user_id;
      },
      set(value) {
        this.$store.commit('SET_USER_ID', value);
      }
    },
    isAuthenticated:{
        get() {
            return this.$store.state.isAuthenticated;
        },
        set(value) {
            this.$store.commit('SET_AUTHENTICATED', value);
        }
    }
  }
};
</script>