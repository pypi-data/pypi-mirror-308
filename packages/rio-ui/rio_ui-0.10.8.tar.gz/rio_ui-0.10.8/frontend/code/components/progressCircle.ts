import { applySwitcheroo } from "../designApplication";
import { ColorSet } from "../dataModels";
import { ComponentBase, ComponentState } from "./componentBase";

export type ProgressCircleState = ComponentState & {
    _type_: "ProgressCircle-builtin";
    progress?: number | null;
    color?: ColorSet;
};

export class ProgressCircleComponent extends ComponentBase {
    declare state: Required<ProgressCircleState>;

    createElement(): HTMLElement {
        let element = document.createElement("div");

        element.innerHTML = `
            <svg viewBox="25 25 50 50">
                <circle class="progress" cx="50" cy="50" r="20"></circle>
            </svg>
        `;
        element.classList.add("rio-progress-circle");
        return element;
    }

    updateElement(
        deltaState: ProgressCircleState,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        // Apply the progress
        if (deltaState.progress !== undefined) {
            if (deltaState.progress === null) {
                this.element.classList.add("spinning");
            } else {
                this.element.classList.remove("spinning");

                let fullCircle = 40 * Math.PI;
                this.element.style.setProperty(
                    "--dasharray",
                    `${deltaState.progress * fullCircle}, ${
                        (1 - deltaState.progress) * fullCircle
                    }`
                );
            }
        }

        // Apply the color
        if (deltaState.color !== undefined) {
            applySwitcheroo(
                this.element,
                deltaState.color === "keep" ? "bump" : deltaState.color
            );
        }
    }
}
