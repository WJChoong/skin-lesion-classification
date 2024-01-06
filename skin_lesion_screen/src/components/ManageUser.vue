<template>
  <div class="container mt-3">
    <div class="card bg-secondary">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h2 class="card-title text-white m-0">User Management</h2>
          <button class="btn btn-success" @click="toggleCreateForm">
            {{ showCreateForm ? 'Hide Form' : 'Create New User' }}
          </button>
        </div>

        <div v-if="userSuccessMessage" class="alert alert-success">
          {{ userSuccessMessage }}
        </div>
        <div v-if="userErrorMessage" class="alert alert-danger">
          {{ userErrorMessage }}
        </div>

        <!-- New User Form -->
        <div v-if="showCreateForm" class="card mb-4">
          <div class="card-body bg-light">
            <h4 class="card-title">Create New User</h4>
            <form @submit.prevent="addUser">
              <div class="form-group">
                <label for="newUserEmail">Email<span class="text-danger">*</span></label>
                <input
                  type="email"
                  class="form-control"
                  id="newUserEmail"
                  v-model="newUser.email"
                  required
                  @input="emailError = !isEmailValid(newUser.email)"
                >
                <!-- Display an error message if the email is not valid -->
                <div v-if="!isEmailValid(newUser.email) && emailError" class="text-danger">Invalid email address</div>
              </div>
              <div class="form-group">
                <label for="newUserName">Name<span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="newUserName"
                  v-model="newUser.name"
                  required
                  @input="nameError = !newUser.name"
                >
                <!-- Display an error message if the name is not filled -->
                <div v-if="!newUser.name && nameError" class="text-danger">Name is required</div>
              </div>
              <div class="form-group mb-3">
                <label for="newUserCountry">Country<span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="newUserCountry"
                  v-model="newUser.country"
                  required
                  @input="countryError = !newUser.country"
                >
                <!-- Display an error message if the country is not filled -->
                <div v-if="!newUser.country && countryError" class="text-danger">Country is required</div>
              </div>
              <button type="submit" class="btn btn-primary" :disabled="creatingUser">
                Add User
                <span v-if="creatingUser" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              </button>
          </form>
          <div>
        </div>
        </div>
      </div>
      <div class="card">
          <div class="card-body bg-light">
              <table class="table table-bordered table-hover rounded mb-3">
                <thead class="thead-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Email</th>
                    <th scope="col">Name</th>
                    <th scope="col">Country</th>
                    <th scope="col">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(user, index) in users" :key="user.id">
                    <td>{{ index + 1 }}</td>
                    <td v-if="!user.editing">{{ user.email }}</td>
                    <td v-else><input type="email" class="form-control" v-model="user.editedEmail" /></td>
                    <td v-if="!user.editing">{{ user.name }}</td>
                    <td v-else><input type="text" class="form-control" v-model="user.editedName" /></td>
                    <td v-if="!user.editing">{{ user.country }}</td>
                    <td v-else><input type="text" class="form-control" v-model="user.editedCountry" /></td>
                    <td>
                      <div class="button-group">  
                        <button v-if="!user.editing" class="btn btn-primary btn-sm" @click="enableEditing(user)" :disabled="editingUser">
                          Edit
                          <span v-if="editingUser" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        </button>
                         <button v-if="user.editing" class="btn btn-success btn-sm" @click="saveEdit(user)" :disabled="editingUser">
                          Save
                          <span v-if="editingUser" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        </button>
                        <button class="btn btn-danger btn-sm" @click="confirmDeletion(user)" :disabled="deletingUser">
                          Delete
                          <span v-if="deletingUser" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="users.length === 0">
                    <td colspan="5" class="text-center">No user data available.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>



<script>
import { mapState } from 'vuex';
const axios = require('axios');

export default {
    data() {
        return {
          users: [],
          showCreateForm: false,
          newUser: { email: '', name: '', country: '' },

          emailError: false,
          nameError: false,
          countryError: false,

          creatingUser: false,
          editingUser: false,
          deletingUser: false,

          userSuccessMessage: '',
          userErrorMessage: '',

          messageTimeout: null,
        };
    },
    created() {
      this.user_id = this.$store.state.user_id;
      if (!this.isAuthenticated || !this.user_id){
          this.$router.push({ name: 'LoginPage' });
      }
      this.getAllUsers();
    },
    computed: {
      ...mapState({
        isAuthenticated: state => state.isAuthenticated,
        user_level: state => state.user_level
      }),
    },
    methods: {
      isEmailValid(email) {
        // Use a regular expression to validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      },
      validateField(field) {
      // Validation logic for each field
        if (field === 'email') {
          this.emailError = !this.isEmailValid(this.newUser.email);
        }
        if (field === 'name') {
          this.nameError = !this.newUser.name;
        }
        if (field === 'country') {
          this.countryError = !this.newUser.country;
        }
      },

      validateForm() {
        // Validate all fields when the form is submitted
        this.validateField('email');
        this.validateField('name');
        this.validateField('country');
      },
      getAllUsers() {
          const apiUrl = 'http://localhost:4040/user/get/all/';
          axios.get(apiUrl)
              .then(response => {
              this.users = response.data.data.map(user => ({ ...user, editing: false }));
              })
              .catch(error => {
              console.error('There was an error fetching the users:', error);
              });
      },
      enableEditing(user) {
          user.editing = true;
          user.editedEmail = user.email;
          user.editedName = user.name;
          user.editedCountry = user.country;
      },
      saveEdit(user) {
        // Validate the edited fields
        if (!this.isEmailValid(user.editedEmail) || !this.isNameValid(user.editedName) || !this.isCountryValid(user.editedCountry)) {
          this.userErrorMessage = 'Please fill all the fields correctly with a valid email address.';
          this.autoHideMessage();
          return;
        }
        
        this.editingUser = true;
        this.clearUserMessages();

        const data = {
          id: user.id,
          name: user.editedName,
          email: user.editedEmail,
          country: user.editedCountry,
        };

        axios.put('http://localhost:4040/user/update/', data)
          .then(response => {
            if (response.data.status === 'success') {
              // Update the user's data in the users array
              user.name = user.editedName;
              user.email = user.editedEmail;
              user.country = user.editedCountry;
              user.editing = false;
              
              this.userSuccessMessage = 'User updated successfully.';
              this.autoHideMessage();
            } else {
              this.userErrorMessage = 'Failed to update user: ' + response.data.message;
              this.autoHideMessage();
            }
          })
          .catch(error => {
            this.userErrorMessage = 'Error updating user: ' + error.message;
            this.autoHideMessage();
          })
          .finally(() => {
            this.editingUser = false;
          });
      },
      confirmDeletion(user) {
          if (confirm(`Are you sure you want to delete ${user.name}?`)) {
              this.deleteUser(user.id);
              this.deletingUser = true;
          }
      },
      async deleteUser(userId) {
        this.deletingUser = true;
        this.clearUserMessages();

        const apiUrl = 'http://localhost:4040/user/delete/'; // Replace with your API endpoint
        const requestData = { id: userId }; // Data to send in the request

        // Make the PUT request to delete the user
        await axios.put(apiUrl, requestData)
                .then(response => {
                  // Check if the deletion was successful (you can use a response status or message)
                  if (response.data.status === 'success') {
                    this.deletingUser = false;
                    this.userSuccessMessage = 'User deleted successfully.';
                    this.autoHideMessage();
                    this.users = this.users.filter(user => user.id !== userId);
                  } else {
                    this.userErrorMessage = 'Failed to delete user.';
                    this.autoHideMessage();
                    this.deletingUser = false;
                  }
                })
                .catch(error => {
                  this.userErrorMessage = 'Error deleting user: ' + error.message;
                  this.autoHideMessage();
                })
                .finally(() => {
                  this.deletingUser = false;
                });
      },
      addUser() {
        // Check if the required fields are filled
        if (this.isEmailValid(this.newUser.email) && this.isNameValid(this.newUser.name) && this.isCountryValid(this.newUser.country)) {
            this.creatingUser = true;
            this.clearUserMessages();
            const apiUrl = 'http://localhost:4040/user/create/';
            axios
                .post(apiUrl, {
                    name: this.newUser.name,
                    email: this.newUser.email,
                    country: this.newUser.country,
                })
                .then((response) => {
                    this.users.push({ ...this.newUser });
                    this.userSuccessMessage = 'User created successfully.';
                    this.autoHideMessage();
                    this.newUser = { email: '', name: '', country: '' }; 
                    this.showCreateForm = false; 
                    this.creatingUser = false;
                })
                .catch((error) => {
                    this.userErrorMessage = 'Error creating user: ' + error.message;
                    this.autoHideMessage();
                })
                .finally(() => {
                  this.creatingUser = false;
                });
        } else {
            this.userErrorMessage = 'Name, email, and country are required.'
            this.autoHideMessage();
        }
      },
      toggleCreateForm() {
          console.log("Opening Create Form");
          this.showCreateForm = !this.showCreateForm;
          this.newUser = { email: '', name: '', country: '' }; // Reset the form fields
      },
      clearUserMessages() {
        this.userSuccessMessage = '';
        this.userErrorMessage = '';
      },
      isEmailValid(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      },
      isNameValid(name) {
        return name.trim().length > 0;
      },
      isCountryValid(country) {
        return country.trim().length > 0;
      },
      autoHideMessage() {
        clearTimeout(this.messageTimeout);
        this.messageTimeout = setTimeout(() => {
            this.userSuccessMessage = '';
            this.userErrorMessage = '';
        }, 2500);
      },
      clearUserMessages() {
          this.userSuccessMessage = '';
          this.userErrorMessage = '';
      },
    },
    mounted() {
      this.getAllUsers();
    }
}
</script>

<style>
.table {
  border-radius: 10px; /* Adjust the radius to your preference */
  margin-bottom: 3rem; /* This adds 3rem of margin to the bottom */
}

.button-group .btn {
  margin-right: 10px;
}

.button-group .btn:last-child {
  margin-right: 0;
}
</style>
