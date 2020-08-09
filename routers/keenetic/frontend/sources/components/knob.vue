<template>
	<div v-if="type==='switch'||type==='checkbox'" :class="type" @click="handleStatusSwitch" tabindex="0">
		<div class="back"><div class="status" :class="currentStatus?'on':'off'"/></div>
		<div v-if="$slots.default" class="label"><slot /></div>
	</div>
	<button v-else @click="handleClick">
		<slot />
	</button>
</template>

<script lang="ts">
import {Vue, Component, Prop, Emit} from 'vue-property-decorator'

@Component
export default class Knob extends Vue {
	@Prop({default: 'button'}) readonly type!: 'button'|'switch'|'checkbox';
	@Prop({default: false}) readonly status!: boolean;

	currentStatus: boolean = this.status;

	@Emit('click')
	handleClick(e:Event) { e.stopPropagation() }

	@Emit('update')
	handleStatusSwitch(e:Event) {
		this.currentStatus = !this.currentStatus;
		this.handleClick(e)
		return this.currentStatus
	}
}
</script>

<style scoped lang="less">
@import "../tools/colors";

button {
	font-family: 'default', serif;
	display: flex;
	align-items: center; justify-content: center;
	width: fit-content; height: fit-content;
	padding: 5px 7px; cursor: pointer;
	border: 1px solid @knob-back-default-active; border-radius: 5px;

	background-color: @knob-back-default-inactive;
	&:hover { background-color: @knob-back-default-hover; }
	&:active { background-color: @knob-back-default-active; }
	transition: background-color 0.3s ease-out;

	&:focus { outline-offset: 2px; outline: @component-focus-outline dashed 1px; }

	color: @main-foreground;
	font-weight: bold;
	* { font-weight: bold }
}

div.switch, div.checkbox {
	display: flex;
	flex-direction: row;
	align-items: center;
	cursor: pointer;

	.back {
		border: 1px solid @knob-back-default-active;
		background-color: @knob-back-default-inactive;
		&:hover { background-color: @knob-back-default-hover; }
		&:active { background-color: @knob-back-default-active; }
		.status { background-color: @knob-back-default-switcher; }
	}

	&:focus { outline-offset: 2px; outline: @component-focus-outline dashed 1px; }

	div.label {
		font-family: 'default', serif;
		padding-left: 5px; padding-bottom: 3px;
	}
}

div.switch {
	.back {
		height: 14px; width: 24px;
		border-radius: 10px;

		.status {
			border-radius: 10px;
			height: 10px; width: 12px;
			position: relative; top: 2px;
			transition: left 0.1s, background-color 0.1s;

			&.on { left: 2px; }
			&.off { left: 10px; background-color: @knob-back-default-active; }
		}
	}
}

div.checkbox {
	.back {
		display: flex; align-items: center; justify-content: center;
		height: 14px; width: 14px;
		border-radius: 5px;

		.status {
			border-radius: 3px;
			height: 10px; width: 10px;
			transition: opacity 0.1s;
			&.on { opacity: 1.0 }
			&.off { opacity: 0.0 }
		}
	}
}
</style>
