<template>
  <div class="container mt-3">
    <div class="card bg-secondary">
      <div class="card-body">
        <h2 class="card-title text-white">Image Categorization</h2>

        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>

        <table class="table table-bordered table-hover rounded mb-3">
          <thead class="thead-dark">
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
                <select v-model="item.selectedClass" class="form-control">
                  <option value="" disabled selected>--- Select Class ---</option>
                  <option v-for="classItem in classes" :value="classItem.id" :key="classItem.id">
                    {{ classItem.name }}
                  </option>
                </select>
                <button class="btn btn-primary mt-2 me-2" @click="classifyImage(item, index)" :disabled="isLoading">Classify</button>
                <button class="btn btn-danger mt-2" @click="confirmDeletion(item, index)" :disabled="isLoading">Delete</button>
              </td>
            </tr>
            <tr v-if="images.length === 0">
              <td colspan="3" class="text-center">There are no images to be categorized.</td>
            </tr>
          </tbody>
        </table>
      </div>
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
        { id: 'UNK', name: 'Unknown' },
      ],
      selectedClass: '',
      isLoading: false,
      successMessage: '',
      errorMessage: '',
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
          this.images = response.data.data.map(image => ({
            ...image,
            selectedClass: ''
          }));
        })
        .catch(error => console.error('Error:', error));
    },
    async classifyImage(item, index) {

      if (!item.selectedClass) {
        this.errorMessage = "Please select a class before classifying.";
        this.autoHideMessage();
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.post('http://localhost:4040/category/images/', {
          user_id: this.user_id,
          image_id: item.id,
          category: item.selectedClass
        });

        this.successMessage = "Image classified successfully.";
        this.autoHideMessage();

        this.loadData()
      } catch (error) {
        console.error('Error in classifying the image:', error);
      } finally {
        this.isLoading = false;
      }
    },
    confirmDeletion(item, index) {
      console.log("item, index", item.id, index);
      if (confirm(`Are you sure you want to delete this image?`)) {
        console.log("Yes, confirmed deletion");
        this.deleteImage(item, index);
        this.isLoading = true;
      }
    },
    deleteImage(item, index) {
      console.log("Delete button triggered")
      try{
        axios
          .put('http://localhost:4040/images/delete/', { id: item.id })
          .then((response) => {
            console.log("Delete process triggered")
            if (response.data.status === "success") {
              this.successMessage = "The image deleted successfully.";
              this.autoHideMessage();
            } else {
              console.error('Failed to delete image:', response.data.message);
              this.errorMessage = 'Failed to delete image: ' + response.data.message;
            }
            this.autoHideMessage();
          })
      } catch(error){
        console.error('Error deleting image:', error);
        this.errorMessage = 'Error occurred while deleting the image.';
        this.autoHideMessage();
      }finally{
        this.isLoading = false;
        this.loadData();
      }
      console.log("Delete process done")
    },
    autoHideMessage() {
      setTimeout(() => {
        this.successMessage = '';
        this.errorMessage = '';
      }, 2500);
    },
  },
  mounted() {
    this.loadData();
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
.table {
  border-radius: 10px;
}

.limited-size-img {
  max-width: 400px;
  max-height: 300px;
}
</style>
