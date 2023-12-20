<template>
  <div class="container mt-3">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Image Uploader</h5>
        <!-- Image preview area -->
        <div v-if="imageData" class="image-preview" v-bind:style="{ backgroundImage: 'url(' + imageData + ')' }"></div>
        <div v-if="!imageData" class="image-preview bg-light d-flex justify-content-center align-items-center">
          <span class="text-muted">No Image Selected</span>
        </div>

        <!-- Hidden file input for triggering the file browser -->
        <input type="file" id="fileInput" ref="fileInput" @change="previewImage" accept="image/*" hidden>

        <!-- Browse and Check buttons -->
        <div class="mt-3">
          <button class="btn btn-primary" @click="browseImage">Browse Image</button>
          <button class="btn btn-secondary" @click="checkImage">Check</button>
        </div>

        <!-- Placeholder for results -->
        <p class="mt-3">Result: {{ resultMessage }}</p>
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

      try {
        const response = await axios.post('http://localhost:4040/api/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // Handle success
        this.resultMessage = response.data.message;
        console.log('Image uploaded successfully:', response);
      } catch (error) {
        // Handle error
        console.error('Error during image upload:', error);
        this.resultMessage = 'Error uploading the image.';
      }
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
