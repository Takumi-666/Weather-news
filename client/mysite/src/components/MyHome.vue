<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Weather-news ♪</h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-btn color="light-blue" @click="goToOtherPage"> スタート </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    goToOtherPage() {
      // ボタンクリック時に他のページに遷移
      this.$router.push("/appWeather");
    },
  },
};
</script>
