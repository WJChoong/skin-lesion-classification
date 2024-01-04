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

        <!-- Hidden file input for triggering the file browser -->
        <input type="file" id="fileInput" ref="fileInput" @change="previewImage" accept="image/*" hidden>

        <!-- Browse and Check buttons -->
        <div class="mt-3">
          <button class="btn btn-primary me-2" @click="browseImage">Browse Image</button>
          <button class="btn btn-primary" @click="checkImage">Check</button>
        </div>

        <!-- Placeholder for results -->
        <p class="mt-3 text-white">Result: {{ resultMessage }}</p>
        <!-- Include other elements for results here -->
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
    };
  },
  methods: {
    browseImage() {
      this.$refs.fileInput.click();
    },
    previewImage(event) {
      this.imageFile = event.target.files[0];
      this.imageData = URL.createObjectURL(this.imageFile);
    },
    async checkImage() {
      if (!this.imageFile) {
        alert('Please select an image to upload');
        return;
      }

      let formData = new FormData();
      formData.append('image', this.imageFile);
      console.log("hello---")

      try {
        const response = await axios.post('http://localhost:4040/images/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // Handle success
        this.resultMessage = response.data.message;
        console.log('Image uploaded successfully:', response);
      } catch (error) {
        // More detailed error handling
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Error data:', error.response.data);
          console.error('Error status:', error.response.status);
          console.error('Error headers:', error.response.headers);
          this.resultMessage = 'Error: ' + error.response.data.message;
        } else if (error.request) {
          // The request was made but no response was received
          console.error('Error request:', error.request);
          this.resultMessage = 'No response from the server.';
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error message:', error.message);
          this.resultMessage = 'Error: ' + error.message;
        }
      }
    },
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
  height: 300px; /* Adjust as needed */
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}
</style>
