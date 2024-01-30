<template>
    <div>
      <select v-model="selectedFolder">
        <option v-for="folder in folders" :key="folder" :value="folder">{{ folder }}</option>
      </select>
      <button @click="runDockerCompose">Run Docker Compose</button>
      <div v-if="output">
        <h3>Output:</h3>
        <pre>{{ output }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        folders: [],
        selectedFolder: '',
        output: ''
      };
    },
    mounted() {
      this.fetchFolders();
    },
    methods: {
      fetchFolders() {
        axios.get('http://127.0.0.1:5000/list-folders')
          .then(response => {
            this.folders = response.data;
          })
          .catch(error => console.error('Error:', error));
      },
      runDockerCompose() {
        axios.post('http://127.0.0.1:5000/run-docker-compose', { folderName: this.selectedFolder })
          .then(response => {
            this.output = response.data.output;
          })
          .catch(error => {
            this.output = 'Error occurred while running Docker Compose.';
            console.error('Error:', error);
          });
      },
    },
  };
  </script>
  