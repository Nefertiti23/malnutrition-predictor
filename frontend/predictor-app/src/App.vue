<script setup>
import TheForm from './components/predictor-form/TheForm.vue';
</script>

<template>
  <header>
    <h1>Child Stunting Predictor</h1>
    <p>
      This predictor uses the LightGBM model, and has been trained on dataset containting
      records of children from Balochistan, Sindh and KPK.
    </p>

    <!-- <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div> -->
  </header>

  <main>
    <TheForm />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    border: solid blanchedalmond 2px;
    display: flex;
    flex-direction: column;
    place-items: center;
    h1 {
      padding-bottom: 20px;
      font-weight: bold;
    }
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
