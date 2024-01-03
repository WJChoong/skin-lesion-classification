<template>
  <div class="container mt-3 mb-3">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h2>User Management</h2>
      <button class="btn btn-success" @click="toggleCreateForm">
        {{ showCreateForm ? '-' : '+' }}
      </button>
    </div>

    <!-- New User Form -->
    <div v-if="showCreateForm" class="mb-4 bg-light p-3 rounded">
      <h4>Create New User</h4>
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
        <button type="submit" class="btn btn-primary">Add User</button>
      </form>
    </div>


    <table class="table table-bordered table-hover">
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
                <button v-if="!user.editing" class="btn btn-primary btn-sm" @click="enableEditing(user)">Edit</button>
                <button v-if="user.editing" class="btn btn-success btn-sm" @click="saveEdit(user)">Save</button>
                <button class="btn btn-danger btn-sm" @click="confirmDeletion(user)">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>



<script>
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
        };
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
      // Check if user data has changed
      if (
        user.email !== user.editedEmail ||
        user.name !== user.editedName ||
        user.country !== user.editedCountry
      ) {
        console.log("ho ho")
        // Prepare the data to send to the API
        const data = {
          id: user.id, // Replace with the actual user ID
          name: user.editedName,
          email: user.editedEmail,
          country: user.editedCountry
        };

        axios
          .put('http://localhost:4040/user/update/', data)
          .then((response) => {
            // Check if the update was successful
            if (response.data.status === 'success') {
              // Update the user's data locally
              user.email = user.editedEmail;
              user.name = user.editedName;
              user.country = user.editedCountry;
              user.editing = false;

              // You can also show a success message to the user if needed
              alert('User updated successfully');
            } else {
              // Handle the case where the API request was successful but the update failed
              // You can display an error message to the user
              alert('Failed to update user: ' + response.data.message);
            }
          })
          .catch((error) => {
            console.error('Error updating user:', error);
            alert('An error occurred while updating user');
          });
      } else {
        user.editing = false;
      }
    },
      confirmDeletion(user) {
          if (confirm(`Are you sure you want to delete ${user.name}?`)) {
              this.deleteUser(user.id);
          }
      },
      deleteUser(userId) {
        // Implement API call to delete user
        const apiUrl = 'http://localhost:4040/user/delete/'; // Replace with your API endpoint
        const requestData = { id: userId }; // Data to send in the request

        // Make the PUT request to delete the user
        axios.put(apiUrl, requestData)
          .then(response => {
            // Check if the deletion was successful (you can use a response status or message)
            if (response.data.status === 'success') {
              // Remove the deleted user from the local array (assuming you have a users array)
              const indexToDelete = this.users.findIndex(user => user.id === userId);
              if (indexToDelete !== -1) {
                this.users.splice(indexToDelete, 1);
              }
            } else {
              // Handle the case where the deletion was not successful
              // You can display an error message to the user if needed
            }
          })
          .catch(error => {
            // Handle any errors that occurred during the API request
            console.error('Error deleting user:', error);
            // You can display an error message to the user if needed
          });
      },
      addUser() {
        // Check if the required fields are filled
        if (this.newUser.email && this.newUser.name && this.newUser.country) {
            const apiUrl = 'http://localhost:4040/user/create/';
            axios
                .post(apiUrl, {
                    name: this.newUser.name,
                    email: this.newUser.email,
                    country: this.newUser.country,
                })
                .then((response) => {
                    // Handle success, you can display a success message or perform other actions here
                    console.log('User created successfully:', response.data);
                    this.users.push({ ...this.newUser });
                    this.newUser = { email: '', name: '', country: '' }; // Reset form
                    this.showCreateForm = false; // Hide the form
                })
                .catch((error) => {
                    // Handle error, you can display an error message or perform other actions here
                    console.error('Error creating user:', error);
                    // You may want to show an error message to the user
                });
        } else {
            // Show an error message if required fields are not filled
            console.error('Name, email, and country are required.');
            // You may want to show an error message to the user
        }
      },
      toggleCreateForm() {
          console.log("Opening Create Form");
          this.showCreateForm = !this.showCreateForm;
          this.newUser = { email: '', name: '', country: '' }; // Reset the form fields
      }
    },
    mounted() {
        this.getAllUsers();
    }
}
</script>

<style>
.button-group .btn {
  margin-right: 10px;
}

.button-group .btn:last-child {
  margin-right: 0;
}
</style>
