# vue-clickoutside
> make a click outside event.

Similar [vue-clickaway](https://github.com/simplesmiler/vue-clickaway), but more simpler. :P


# Installation
```shell
npm i vue-clickoutside -D
```

# Demo
![demo gif](http://g.recordit.co/pDjxMhZ1IA.gif)

# Quick Start
```javascript
import Vue from 'vue'
import VueClickoutside from 'vue-clickoutside'

Vue.use(VueClickoutside)

// or custom directive id
Vue.directive('v-clickoutside', VueClickoutside)
```

```html
<div v-clickoutside="show = false" class="box">
  <button @click="show = true">click me</button>
  <div v-show="show">dropdown</div>
</div>
```

# Development
If you using NPM 3.x, these will not be automatically installed.

- jasmine-core *
- phantomjs-prebuilt ^1.9

# License
[MIT](https://opensource.org/licenses/MIT)
