<template>
    <h3>Hello Home</h3>
</template>

<script>
    import axios from 'axios'

    export default {
        name:'Home',
        async created() {
            const response = await axios.get('user', {
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                }
            });

            console.log(response);
        }
    }
</script>