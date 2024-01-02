<template>
  <div class="container mt-3 mb-3">
    <h2>User Management</h2>
    <table class="table table-bordered table-hover">
      <thead class="thead-dark">
        <tr>
          <th>#</th> <!-- Column for the index -->
          <th>Email</th>
          <th>Name</th>
          <th>Country</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="user.id">
            <td>{{ index + 1 }}</td> <!-- Displaying the index starting from 1 -->
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.country }}</td>
            <td>
                <div class="button-group">
                    <button class="btn btn-sm btn-primary" @click="confirmEdit(user)">Edit</button>
                    <button class="btn btn-sm btn-danger" @click="confirmDeletion(user.id)">Delete</button>
                </div>
            </td>
        </tr>
      </tbody>
    </table>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="modal" tabindex="-1" role="dialog" id="editUserModal">
        <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title">Confirm Action</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            <p>{{ editModalMessage }}</p>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="modalConfirm">Confirm</button>
            </div>
        </div>
        </div>
    </div>

    <div v-if="showCreateModal" class="modal" tabindex="-1" role="dialog" id="createUserModal">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Create User</h5>
                <button type="button" class="close" @click="closeCreateModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <!-- Add form fields for creating a new user here -->
                <!-- Bind them to the newUser data property -->
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeCreateModal">Cancel</button>
                <button type="button" class="btn btn-primary" @click="createUser">Create User</button>
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
      users: [],
      editModalMessage: '',

      // Modal visibility flags
      showEditModal: false,
      showDeleteModal: false,
      showCreateModal: false,

      // Modal messages
      editModalMessage: '',
      deleteModalMessage: '',
      createModalMessage: '',

      // User data
      userToEdit: null,
      userToDelete: null,
      newUser: {}, // Initialize as empty or with default values
    };
  },
  methods: {
    getAllUsers() {
      const apiUrl = 'http://localhost:4040/user/get/all/'; // Replace with the actual URL to your API
      axios.get(apiUrl)
        .then(response => {
          this.users = response.data.data; // Adjust if your response format is different
        })
        .catch(error => {
          console.error('There was an error fetching the users:', error);
        });
    },
    confirmEdit(user) {
        this.userToEdit = user;
        this.modalMessage = `Are you sure you want to edit the user: ${user.name}?`;
        $('#editUserModal').modal('show'); // Changed to match the modal's ID
    },
    confirmDeletion(userId) {
      this.userToDelete = userId;
      this.modalMessage = 'Are you sure you want to delete this user?';
      $('#confirmationModal').modal('show');
    },
    modalConfirm() {
      if (this.userToEdit) {
        this.editUser();
      } else if (this.userToDelete) {
        this.deleteUser();
      }
      $('#confirmationModal').modal('hide');
    },
    addUser() {
      const apiUrl = '/path/to/your/createUser/endpoint'; // Replace with actual URL
      axios.post(apiUrl, this.newUser)
        .then(response => {
          // Handle the success response
          this.getAllUsers(); // Refresh the list of users
        })
        .catch(error => {
          // Handle the error response
          console.error('Error creating user:', error);
        });
    },
    updateUser() {
      const apiUrl = 'http://localhost:4040/user/update/'; // Replace with actual URL
      axios.put(apiUrl, this.userToEdit)
        .then(response => {
          // Handle the success response
          this.getAllUsers(); // Refresh the list of users
        })
        .catch(error => {
          // Handle the error response
          console.error('Error updating user:', error);
        });
    },
    deleteUser() {
      const apiUrl = 'http://localhost:4040/user/delete/'; // Replace with actual URL
      axios.put(apiUrl, { id: this.userToDelete })
        .then(response => {
          // Handle the success response
          this.getAllUsers(); // Refresh the list of users
        })
        .catch(error => {
          // Handle the error response
          console.error('Error deleting user:', error);
        });
    },

    // Methods for Delete Modal
    confirmDeletion(user) {
      this.userToDelete = user;
      this.deleteModalMessage = `Are you sure you want to delete ${user.name}?`;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
    },
    deleteUser() {
      // Implement your logic to delete user
      this.closeDeleteModal();
    },

    // Method for edit model
    confirmEdit(user) {
      this.userToEdit = user;
      this.editModalMessage = `Are you sure you want to edit the user: ${user.name}?`;
      this.showEditModal = true;
    },
    closeModal() {
      this.showEditModal = false;
    },
    editUser() {
      this.closeModal();
    },

    // API for create model
    openCreateModal() {
      this.createModalMessage = 'Enter details for the new user.';
      this.showCreateModal = true;
    },
    closeCreateModal() {
      this.showCreateModal = false;
    },
    createUser() {
      // Implement your logic to create a new user
      this.closeCreateModal();
    },
  },
  mounted() {
    this.getAllUsers();
  }
}
</script>

<style>
.button-group .btn {
  margin-right: 10px; /* Adds margin to the right of each button */
}

.button-group .btn:last-child {
  margin-right: 0; /* Removes margin from the right of the last button */
}
</style>
