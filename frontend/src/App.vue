<template>
  <div id="app">
    <DockerComposeRunner/>
    </div>
</template>

<script>
import DockerComposeRunner from './components/DockerComposeRunner.vue';

export default {
  name: 'App',
  components: {
    DockerComposeRunner
  }
}
</script>

<style>
</style>
