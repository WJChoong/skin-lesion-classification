<template>
  <div class="container mt-4">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>#</th>
          <th>Image</th>
          <th>Classify</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in images" :key="item.id">
          <th>{{ index + 1 }}</th>
          <td><img :src="item.image" class="img-fluid" :alt="'Image ' + (index + 1)"></td>
          <td>
            <select v-model="selectedClass" class="form-control">
              <option value="">Select Class</option>
              <option v-for="classItem in isicClasses" :value="classItem.id" :key="classItem.id">
                {{ classItem.name }}
              </option>
            </select>
            <button class="btn btn-primary mt-2" @click="classifyImage(item, index)">Classify</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
const axios = require('axios')

export default {
  data() {
    return {
      images: [],
      classes: [
        "Melanoma",
        "Melanocytic Nevus",
        "Basal Cell Carcinoma",
        "Actinic Keratosis",
        "Benign Keratosis",
        "Dermatofibroma",
        "Vascular Lesion",
        "Squamous Cell Carcinoma"
      ]
    };
  },
  methods: {
    classifyImage(item, index) {
      if (!item.selectedClass) {
        alert('Please select a class.');
        return;
      }

      const dataToSend = {
        imageId: item.id,
        selectedClass: item.selectedClass,
        userId: this.userId
      };

      axios.post('http://localhost:8000/api/classify/image/', dataToSend)
        .then(() => {
          this.images.splice(index, 1); // Remove the image from the array
        })
        .catch(error => console.error('Error:', error));
    }
  },
  mounted() {
    axios.get('http://localhost:4040/api/get/images/')
        .then(response => {
        console.log(response.data.images); // Log to check the URLs
        this.images = response.data.images;
        })
        .catch(error => console.error('Error:', error));
    }
};
</script>

<style>
/* Additional custom styles (if needed) */
</style>
