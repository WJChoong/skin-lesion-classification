<template>
    <div class="container">
    <div class="card mt-4 bg-secondary">
      <div class="card-body">
        <h5 class="card-title text-white">Upload Your Image Here</h5>
        <!-- Image preview area -->
        <div v-if="imageData" class="image-preview" v-bind:style="{ backgroundImage: 'url(' + imageData + ')' }"></div>
        <div v-if="!imageData" class="image-preview bg-white d-flex justify-content-center align-items-center">
          <span class="text-muted">No Image Selected</span>
        </div>

        <input type="file" id="fileInput" ref="fileInput" @change="previewImage" accept="image/*" hidden>

        <div class="mt-3">
            <button class="btn btn-primary me-2" @click="browseImage" :disabled="isLoading">Browse Image</button>
            <button class="btn btn-primary" @click="checkImage">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Checking...' : 'Check' }}
            </button>
        </div>

        <p class="mt-3 text-white">Result: {{ resultMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios');

export default {
  data() {
    return {
      imageFile: null,
      imageData: null,
      resultMessage: null,
      isLoading: false
    };
  },
  methods: {
    browseImage() {
      this.resultMessage = null;
      this.$refs.fileInput.click();
    },
    previewImage(event) {
      this.imageFile = event.target.files[0];
      this.imageData = URL.createObjectURL(this.imageFile);
      this.resultMessage = null;
    },
    async checkImage() {
      if (!this.imageFile) {
        alert('Please select an image to upload');
        return;
      }

      this.isLoading = true;
      let formData = new FormData();
      formData.append('image', this.imageFile);

      try {
        const response = await axios.post('http://localhost:4040/images/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.resultMessage = response.data.message;
      } catch (error) {
        this.handleError(error);
      } finally {
        this.isLoading = false;
      }
    },
    handleError(error) {
      if (error.response) {
        this.resultMessage = 'Error: ' + error.response.data.message;
      } else if (error.request) {
        this.resultMessage = 'No response from the server.';
      } else {
        this.resultMessage = 'Error: ' + error.message;
      }
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },

};
</script>

<style scoped>
.image-preview {
  width: 100%;
  height: 300px; 
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}
</style>
