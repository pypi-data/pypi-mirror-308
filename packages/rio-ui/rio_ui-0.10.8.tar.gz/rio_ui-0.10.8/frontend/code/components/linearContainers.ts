import { pixelsPerRem } from "../app";
import { componentsById } from "../componentManagement";
import { ComponentId } from "../dataModels";
import { OnlyResizeObserver, zip } from "../utils";
import { ComponentBase, ComponentState } from "./componentBase";

export type LinearContainerState = ComponentState & {
    _type_: "Row-builtin" | "Column-builtin";
    children?: ComponentId[];
    spacing?: number;
    proportions?: "homogeneous" | number[] | null;
};

const PROPORTIONS_SPACER_SIZE = 30;

export abstract class LinearContainer extends ComponentBase {
    declare state: Required<LinearContainerState>;

    index = -1; // 0 for Rows, 1 for Columns
    sizeAttribute = ""; // 'width' for Rows, 'height' for Columns

    // All this stuff is needed for the `proportions`.
    //
    // When proportions are enabled, we must execute JS code whenever the
    // natural size of a child element changes. We have `naturalSizeObservers.ts`
    // for that, but wrapping every single child element in one of those would
    // be horribly inefficient. Quick summary of how it's done:
    //
    // - Make the flexbox slightly larger than it needs to be
    // - Add an invisible spacer element at the end to fill up this extra space
    // - Calculate the `flex-grow` of every child element so that it ends up
    //   with the desired proportion
    // - Whenever a child's natural size changes, the spacer will grow or
    //   shrink. We can detect this with a ResizeObserver.
    private helperElement: HTMLElement;
    private childContainer: HTMLElement;
    private proportionsSpacer: HTMLElement | null = null;
    private proportionNumbers: number[] = [];
    private totalProportions: number = 0;
    private childNaturalSizes: number[] = [];
    private selfResizeObserver: OnlyResizeObserver | null = null;
    private spacerResizeObserver: OnlyResizeObserver | null = null;

    onDestruction(): void {
        super.onDestruction();

        if (this.selfResizeObserver !== null) {
            this.selfResizeObserver.disconnect();
        }

        if (this.spacerResizeObserver !== null) {
            this.spacerResizeObserver.disconnect();
        }
    }

    createElement(): HTMLElement {
        let element = document.createElement("div");
        element.classList.add("rio-linear-container");

        this.helperElement = document.createElement("div");
        element.appendChild(this.helperElement);

        this.childContainer = document.createElement("div");
        this.helperElement.appendChild(this.childContainer);

        return element;
    }

    updateElement(
        deltaState: LinearContainerState,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        // Children
        if (deltaState.children !== undefined) {
            this.replaceChildren(
                latentComponents,
                deltaState.children,
                this.childContainer,
                true
            );

            // Make sure the `proportionsSpacer` is at the end
            if (this.proportionsSpacer !== null) {
                this.childContainer.appendChild(this.proportionsSpacer);
            }
        }

        // Spacing
        if (deltaState.spacing !== undefined) {
            this.childContainer.style.gap = `${deltaState.spacing}rem`;
        }

        // Proportions
        if (deltaState.proportions !== undefined) {
            if (deltaState.proportions === null) {
                if (this.proportionsSpacer !== null) {
                    this.element.classList.remove("has-proportions");

                    this.helperElement.style.removeProperty(
                        `min-${this.sizeAttribute}`
                    );
                    this.childContainer.style.removeProperty(
                        this.sizeAttribute
                    );

                    this.selfResizeObserver!.disconnect();
                    this.selfResizeObserver = null;

                    this.spacerResizeObserver!.disconnect();
                    this.spacerResizeObserver = null;

                    this.proportionsSpacer.remove();
                    this.proportionsSpacer = null;
                }
            } else {
                if (this.proportionsSpacer === null) {
                    this.element.classList.add("has-proportions");

                    this.selfResizeObserver = new OnlyResizeObserver(
                        this.childContainer,
                        this.updateChildProportions.bind(this)
                    );

                    // Add the spacer element
                    this.proportionsSpacer = document.createElement("div");
                    this.proportionsSpacer.classList.add(
                        "rio-not-a-child-component"
                    );
                    this.proportionsSpacer.style.flexGrow = `${PROPORTIONS_SPACER_SIZE}`;
                    this.childContainer.appendChild(this.proportionsSpacer);

                    this.spacerResizeObserver = new OnlyResizeObserver(
                        this.proportionsSpacer,
                        this._onChildNaturalSizeChanged.bind(this)
                    );
                }
            }
        }

        // Update the CSS if necessary
        if (
            deltaState.children !== undefined ||
            deltaState.proportions !== undefined ||
            deltaState.spacing !== undefined
        ) {
            Object.assign(this.state, deltaState);

            if (this.state.proportions === null) {
                this.updateChildGrows();
            } else {
                // Not entirely sure why this delay is needed, but we suspect
                // it's because ResizeObservers can only trigger once per frame
                // or something like that. So it triggers too early (before the
                // child components did `updateElement`) and then doesn't run
                // again.
                //
                // Without this workaround proportions were often wrong, and it
                // has definitely improved the situation immensely, but I doubt
                // that the underlying problem is really solved.
                requestAnimationFrame(() => {
                    this.updateMinSize();
                    this.updateChildProportions();
                });
            }
        }
    }

    onChildGrowChanged(): void {
        if (this.state.proportions === null) {
            this.updateChildGrows();
        }
    }

    private updateChildGrows(): void {
        // Set the children's `flex-grow`
        let hasGrowers = false;
        for (let [index, childId] of this.state.children.entries()) {
            let childComponent = componentsById[childId]!;
            let childWrapper = this.childContainer.children[
                index
            ] as HTMLElement;

            if (childComponent.state._grow_[this.index]) {
                hasGrowers = true;
                childWrapper.style.flexGrow = "1";
            } else {
                childWrapper.style.flexGrow = "0";
            }
        }

        // If nobody wants to grow, all of them do
        if (!hasGrowers) {
            for (let childWrapper of this.childContainer.children) {
                (childWrapper as HTMLElement).style.flexGrow = "1";
            }
        }
    }

    private updateMinSize(): void {
        if (this.state.children.length === 0) {
            this.proportionNumbers = [];
            this.totalProportions = 0;
            this.childNaturalSizes = [];

            this.helperElement.style.setProperty(
                `min-${this.sizeAttribute}`,
                "0"
            );
            return;
        }

        this.spacerResizeObserver!.disable();

        // Get every child's natural size
        this.childContainer.style.setProperty(
            this.sizeAttribute,
            "min-content"
        );
        this.childContainer.style.setProperty(`min-${this.sizeAttribute}`, "0");

        this.childNaturalSizes = [];
        for (let child of this.childContainer.children) {
            let size = child.getBoundingClientRect()[this.sizeAttribute];
            this.childNaturalSizes.push(size);
        }
        this.childNaturalSizes.pop(); // The last one's the spacer, remove it

        this.childContainer.style.setProperty(
            this.sizeAttribute,
            `calc(100% + ${PROPORTIONS_SPACER_SIZE}px + ${this.state.spacing}rem)`
        );
        this.childContainer.style.removeProperty(`min-${this.sizeAttribute}`);

        // Sum up the proportions
        this.proportionNumbers =
            this.state.proportions === "homogeneous"
                ? new Array(this.children.size).fill(1)
                : this.state.proportions!;

        this.totalProportions = 0;
        for (let proportion of this.proportionNumbers) {
            this.totalProportions += proportion;
        }

        // Calculate the minimum size we need to fit all children
        let pixelPerProportion = 0;
        for (let [naturalSize, proportion] of zip(
            this.childNaturalSizes,
            this.proportionNumbers
        )) {
            pixelPerProportion = Math.max(
                pixelPerProportion,
                naturalSize / proportion
            );
        }

        let containerMinSize = pixelPerProportion * this.totalProportions;
        this.helperElement.style[this.index === 0 ? "minWidth" : "minHeight"] =
            `${containerMinSize}px`;

        this.spacerResizeObserver!.enable();
    }

    private updateChildProportions(): void {
        this.spacerResizeObserver!.disable();

        let rect = this.element.getBoundingClientRect();
        let availableSpace =
            rect[this.sizeAttribute] - this.state.spacing * pixelsPerRem;

        let i = 0;
        for (let childElement of this.childContainer.children) {
            if (i >= this.proportionNumbers.length) {
                break;
            }

            let desiredSize =
                (availableSpace * this.proportionNumbers[i]) /
                this.totalProportions;

            (childElement as HTMLElement).style.flexGrow = `${
                desiredSize - this.childNaturalSizes[i]
            }`;

            i++;
        }

        this.spacerResizeObserver!.enable();
    }

    private _onChildNaturalSizeChanged(): void {
        this.updateMinSize();
        this.updateChildProportions();
    }
}

export class RowComponent extends LinearContainer {
    index = 0;
    sizeAttribute = "width";

    createElement(): HTMLElement {
        let element = super.createElement();
        element.classList.add("rio-row");
        return element;
    }
}

export class ColumnComponent extends LinearContainer {
    index = 1;
    sizeAttribute = "height";

    createElement(): HTMLElement {
        let element = super.createElement();
        element.classList.add("rio-column");
        return element;
    }
}
