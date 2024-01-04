<template>
  <div class="container">
    <div class="mt-4 bg-secondary">
      <div v-if="isLoading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <table class="table table-bordered rounded">
        <thead>
          <tr>
            <th>#</th>
            <th>Image</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in images" :key="item.id">
            <th>{{ index + 1 }}</th>
            <td>
              <img :src="item.image" class="img-fluid limited-size-img" :alt="'Image ' + (index + 1)" />
            </td>
            <td>
              <select v-model="selectedClass" class="form-control">
                <option value="" disabled selected>--- Select Class ---</option> <!-- Placeholder option -->
                <option v-for="classItem in classes" :value="classItem.id" :key="classItem.id">
                  {{ classItem.name }}
                </option>
              </select>
              <button class="btn btn-primary mt-2 me-2" @click="classifyImage(item, index)">Classify</button>
              <button class="btn btn-danger mt-2" @click="deleteImage(item, index)">Delete</button>
            </td>
          </tr>
          <tr v-if="images.length === 0">
            <td colspan="3" class="text-center">There are no images to be categorized.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  data() {
    return {
      images: [],
      classes: [
        { id: 'MEL', name: 'Melanoma' },
        { id: 'NV', name: 'Melanocytic Nevus' },
        { id: 'BCC', name: 'Basal Cell Carcinoma' },
        { id: 'AK', name: 'Actinic Keratosis' },
        { id: 'BKL', name: 'Benign Keratosis' },
        { id: 'DF', name: 'Dermatofibroma' },
        { id: 'VASC', name: 'Vascular Lesion' },
        { id: 'SCC', name: 'Squamous Cell Carcinoma' },
      ],
      selectedClass: '',
      isLoading: false,
    };
  },
  created() {
    this.user_id = this.$store.state.user_id;
    if (!this.isAuthenticated || !this.user_id){
        this.$router.push({ name: 'LoginPage' });
    }
  },
  methods: {
    loadData() {
      axios.get('http://localhost:4040/images/get/')
      .then(response => {
        this.images = response.data.data
      })
      .catch(error => console.error('Error:', error));
    },
    async classifyImage(item, index) {
      const selectedClass = this.selectedClass;
      const imageId = item.id;

      if (!selectedClass) {
        alert("Please select a class.");
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.post('http://localhost:4040/category/images/', {
          user_id: this.user_id,
          image_id: imageId,
          category: selectedClass
        });

        this.loadData()
      } catch (error) {
        console.error('Error in classifying the image:', error);
      } finally {
        this.isLoading = false; // Stop loading regardless of outcome
      }
    },
    deleteImage(item, index) {
      // Make a DELETE request to the Django API
      axios
        .put('http://localhost:4040/images/delete/', { id: item.id }) // Replace with your actual API endpoint
        .then((response) => {
          // Check the response and handle success or failure as needed
          if (response.status === "success") {
            this.loadData();
          } else {
            // Handle API error (e.g., image not found)
            alert('Failed to delete image: ' + response.data.message);
          }
        })
        .catch((error) => {
          // Handle network or other errors
          console.error('Error deleting image:', error);
        });
    },
  },
  mounted() {
    this.loadData();
    this.isLoading = false;
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

<style>
.limited-size-img {
  max-width: 400px;
  max-height: 300px;
}
</style>
