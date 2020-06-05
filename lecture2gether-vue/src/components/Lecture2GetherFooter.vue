<template>
    <v-footer>
        <v-spacer></v-spacer>
        <img src="/img/icons/GitHub.svg" alt="GitHub logo" class="mr-2"/>
        <a href="https://github.com/TheNerdful8/Lecture2Gether" class="footer-link">Lecture2Gether on Github</a>
        <v-spacer></v-spacer>
    </v-footer>
</template>
<script lang="ts">
export default {
    name: 'Lecture2GetherFooter',
};
</script>
<style lang="scss">
    .footer-link {
        color: #222222 !important;
    }

    .footer-link:link {
        text-decoration: none;
    }

    .footer-link:hover {
        text-decoration: underline;
    }
</style>
