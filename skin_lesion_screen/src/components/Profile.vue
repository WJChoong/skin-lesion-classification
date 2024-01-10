<template>
  <div class="container mt-5">
    <div class="row">
      <!-- User Details Form Section -->
      <div class="col-md-6 mb-3">
        <div class="card bg-secondary">
          <div class="card-body">
            <h5 class="card-title text-white">Update User Details</h5>
            <!-- Form elements here -->
            <form @submit.prevent="updateDetails">
              <div class="form-group text-white">
                <label for="name">Name</label>
                <input type="text" id="name" class="form-control" v-model="user.name" :readonly="!editing">
              </div>
              <div class="form-group text-white">
                <label for="email">Email</label>
                <input type="email" id="email" class="form-control" v-model="user.email" :readonly="!editing">
              </div>
              <div class="form-group text-white">
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
                <button type="submit" class="btn btn-success mt-3" style="margin-right: 8px;" :disabled="updateUserDetailsLoading">
                  Save Changes
                  <span v-if="updateUserDetailsLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
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
        <div class="card bg-secondary">
          <div class="card-body">
            <h5 class="card-title text-white">Change Password</h5>
            <!-- Form elements here -->
            <form @submit.prevent="changePassword">
                <div class="form-group text-white">
                    <label for="oldPassword">Old Password</label>
                    <input type="password" id="oldPassword" class="form-control" v-model="password.oldPassword">
                </div>
                <div class="form-group text-white">
                    <label for="newPassword">New Password</label>
                    <input type="password" id="newPassword" class="form-control" v-model="password.newPassword">
                </div>
                <div class="form-group text-white">
                    <label for="confirmNewPassword">Re-enter New Password</label>
                    <input type="password" id="confirmNewPassword" class="form-control" v-model="password.confirmNewPassword">
                </div>
                <div v-if="passwordChangeSuccessMessage" class="alert alert-success mt-3">
                  {{ passwordChangeSuccessMessage }}
                </div>
                <div v-if="passwordChangeErrorMessage" class="alert alert-danger mt-3">
                  {{ passwordChangeErrorMessage }}
                </div>
                <button type="submit" class="btn btn-primary mt-3" :disabled="changePasswordLoading">
                  Change Password
                  <span v-if="changePasswordLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios');

export default {
  data() {
    return {
      editing: false,
      loading: false,
      successMessage: '',
      errorMessage: '',
      originalUserData: null,
      user: {
        name: '',
        email: '',
        country: ''
      },
      password: {
        oldPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      },
      passwordChangeSuccessMessage: '',
      passwordChangeErrorMessage: '',
      updateUserDetailsLoading: false,
      changePasswordLoading: false,
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
          this.originalUserData = { ...this.user };
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
      if (!this.canSubmit) {
        this.errorMessage = "Please fill all the fields correctly.";
        this.autoHideMessage();
        return;
      }
      this.updateUserDetailsLoading = true;
      try {
        console.log("user_id", this.user_id)
        const response = await axios.put('http://localhost:4040/user/update/', {
          id: this.user_id,
          name: this.user.name,
          email: this.user.email,
          country: this.user.country
        });
        if (response.data.status === 'success') {
            this.successMessage = 'Operation successful!';
        } else {
            this.errorMessage = 'An error occurred. Please try again.';
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
      this.updateUserDetailsLoading = false;
      this.editing = false;
      this.autoHideMessage()
    },
    async changePassword() {
      this.changePasswordLoading = true;

      // Check if any of the password fields are blank
      if (!this.password.oldPassword.trim() || 
          !this.password.newPassword.trim() || 
          !this.password.confirmNewPassword.trim()) {
        this.passwordChangeErrorMessage = "All fields are required.";
        this.changePasswordLoading = false;
        this.autoHidePasswordChangeMessage();
        return;
      }

      // Check if the new password and confirm new password match
      if (this.password.newPassword !== this.password.confirmNewPassword) {
        this.passwordChangeErrorMessage = "New passwords are not the same.";
        this.changePasswordLoading = false;
        this.autoHidePasswordChangeMessage();
        return;
      }

      // Check if the old password and new password are the same
      if (this.password.oldPassword === this.password.newPassword) {
        this.passwordChangeErrorMessage = "New password cannot be the same as the old password.";
        this.changePasswordLoading = false;
        this.autoHidePasswordChangeMessage();
        return;
      }

      try {
        const response = await axios.put('http://localhost:4040/auth/change/', {
          user_id: this.user_id,
          old_password: this.password.oldPassword,
          new_password: this.password.newPassword
        });

        // On success
        if (response.data.status === 'success') {
          this.passwordChangeSuccessMessage = "Password successfully changed.";
          this.password.oldPassword = '';
          this.password.newPassword = '';
          this.password.confirmNewPassword = '';
          
        } else {
          // Handle failure
          this.passwordChangeErrorMessage = response.data.message || 'Failed to change password. Please try again.';
          this.password.oldPassword = '';
          this.password.newPassword = '';
          this.password.confirmNewPassword = '';
        }
      } catch (error) {
        // Handle the error
        console.error('An error occurred:', error);
        this.passwordChangeErrorMessage = 'An unexpected error occurred. Please try again.';
      }
      this.changePasswordLoading = false;
      this.autoHidePasswordChangeMessage();
    },
    autoHideMessage() {
      setTimeout(() => {
        this.successMessage = '';
        this.errorMessage = '';
      }, 2500);
    },
    autoHidePasswordChangeMessage() {
      setTimeout(() => {
        this.passwordChangeSuccessMessage = '';
        this.passwordChangeErrorMessage = '';
      }, 2500);
    },
    enableEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.user = { ...this.originalUserData };
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
    },
    isNameValid() {
      return this.user.name.trim() !== '';
    },
    isEmailValid() {
      const pattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
      return pattern.test(this.user.email);
    },
    isCountryValid() {
      return this.user.country.trim() !== '';
    },
    canSubmit() {
      console.log("this.isNameValid", this.isNameValid)
      console.log("this.isEmailValid", this.isEmailValid)
      console.log("this.isCountryValid", this.isCountryValid)
      return this.isNameValid && this.isEmailValid && this.isCountryValid;
    },
    isPasswordValid() {
      return this.password.oldPassword.trim() !== '' &&
             this.password.newPassword.trim() !== '' &&
             this.password.confirmNewPassword.trim() !== '' &&
             this.password.newPassword === this.password.confirmNewPassword &&
             this.password.oldPassword !== this.password.newPassword;
    }
  }
};
</script>