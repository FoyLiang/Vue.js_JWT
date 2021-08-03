<template>
    <nav class="navbar navbar-expand navbar-light fixed-top">
        <div class="container">
            <router-link to="/" class="navbar-brand">Home</router-link>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ml-auto" v-if="!user">
                    <li class="nav-item">
                        <router-link to="./login" class="nav-link">Login</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="./register" class="nav-link">Sing up</router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto" v-if="user">
                    <li>
                        <a href="javascript:void(0)" @click="handleClick" class="nav-link">logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: 'Nav',
        props: ['user'],
        methods: {
            handleClick(){
                localStorage.removeItem('token');
                this.$router.push('/');
            }
        }
    }
</script>