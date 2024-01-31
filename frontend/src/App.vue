<template>
  <div id="app">
    <DockerComposeRunner/>
    <DockerImage/>
    </div>
</template>

<script>
import DockerComposeRunner from './components/DockerComposeRunner.vue';
import DockerImage from './components/DockerImage.vue';

export default {
  name: 'App',
  components: {
    DockerComposeRunner,
    DockerImage
  }
}
</script>

<style>
</style>
