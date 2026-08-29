// ==========================================
// TO-DO LIST JAVASCRIPT
// ==========================================


// ==========================================
// ADD TASK
// ==========================================

const taskForm =
    document.getElementById("taskForm");


if (taskForm) {

    taskForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const input =
                taskForm.querySelector(
                    "input[name='title']"
                );


            const taskTitle =
                input.value.trim();


            if (taskTitle === "") {

                alert(
                    "Please enter a task."
                );

                return;
            }


            try {

                const response =
                    await fetch(
                        "/tasks",
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/x-www-form-urlencoded"

                            },

                            body:
                                new URLSearchParams({

                                    title: taskTitle

                                })

                        }
                    );


                if (!response.ok) {

                    alert(
                        "Failed to create task."
                    );

                    return;
                }


                console.log(
                    "Task created successfully"
                );


                input.value = "";


                // Reload the page
                // so the new task appears

                window.location.reload();


            }
            catch (error) {

                console.error(
                    "Add task error:",
                    error
                );


                alert(
                    "Something went wrong."
                );

            }

        }
    );

}



// ==========================================
// DELETE TASK
// ==========================================

const deleteForms =
    document.querySelectorAll(
        "form[action*='/delete']"
    );


deleteForms.forEach(
    function (form) {


        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const confirmed =
                    confirm(
                        "Are you sure you want to delete this task?"
                    );


                if (!confirmed) {

                    return;

                }


                const url =
                    form.getAttribute(
                        "action"
                    );


                try {

                    const response =
                        await fetch(
                            url,
                            {
                                method: "POST"
                            }
                        );


                    if (!response.ok) {

                        alert(
                            "Failed to delete task."
                        );

                        return;
                    }


                    const data =
                        await response.json();


                    console.log(
                        data.message
                    );


                    const taskItem =
                        form.closest(
                            ".task-item"
                        );


                    if (taskItem) {

                        taskItem.remove();

                    }


                }
                catch (error) {

                    console.error(
                        "Delete task error:",
                        error
                    );


                    alert(
                        "Something went wrong."
                    );

                }

            }
        );

    }
);



// ==========================================
// COMPLETE TASK
// ==========================================

const completeForms =
    document.querySelectorAll(
        "form[action*='/complete']"
    );


completeForms.forEach(
    function (form) {


        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const confirmed =
                    confirm(
                        "Mark this task as completed?"
                    );


                if (!confirmed) {

                    return;

                }


                const url =
                    form.getAttribute(
                        "action"
                    );


                try {

                    const response =
                        await fetch(
                            url,
                            {
                                method: "POST"
                            }
                        );


                    if (!response.ok) {

                        alert(
                            "Failed to complete task."
                        );

                        return;
                    }


                    const data =
                        await response.json();


                    console.log(
                        data.message
                    );


                    const taskItem =
                        form.closest(
                            ".task-item"
                        );


                    if (taskItem) {


                        const taskTitle =
                            taskItem.querySelector(
                                ".task-title"
                            );


                        if (taskTitle) {


                            const title =
                                taskTitle.textContent.trim();


                            taskTitle.innerHTML =
                                "✓ " + title;


                            taskTitle.classList.add(
                                "completed-task"
                            );

                        }


                        // Remove COMPLETE button

                        form.remove();

                    }


                }
                catch (error) {

                    console.error(
                        "Complete task error:",
                        error
                    );


                    alert(
                        "Something went wrong."
                    );

                }

            }
        );

    }
);



// ==========================================
// EDIT TASK
// ==========================================

const editButtons =
    document.querySelectorAll(
        ".edit-button"
    );


editButtons.forEach(
    function (button) {


        button.addEventListener(
            "click",
            async function () {


                const taskId =
                    button.getAttribute(
                        "data-task-id"
                    );


                const oldTitle =
                    button.getAttribute(
                        "data-task-title"
                    );


                const newTitle =
                    prompt(
                        "Edit your task:",
                        oldTitle
                    );


                // User clicked Cancel

                if (newTitle === null) {

                    return;

                }


                const updatedTitle =
                    newTitle.trim();


                if (updatedTitle === "") {

                    alert(
                        "Task title cannot be empty."
                    );

                    return;

                }


                try {


                    const response =
                        await fetch(
                            `/tasks/${taskId}/edit`,
                            {

                                method: "POST",

                                headers: {

                                    "Content-Type":
                                        "application/x-www-form-urlencoded"

                                },

                                body:
                                    new URLSearchParams({

                                        title:
                                            updatedTitle

                                    })

                            }
                        );


                    if (!response.ok) {


                        let errorMessage =
                            "Failed to update task.";


                        try {

                            const errorData =
                                await response.json();


                            errorMessage =
                                errorData.detail ||
                                errorMessage;

                        }
                        catch {

                            // Ignore JSON parsing error

                        }


                        alert(
                            errorMessage
                        );


                        return;

                    }


                    const data =
                        await response.json();


                    console.log(
                        data.message
                    );


                    const taskItem =
                        button.closest(
                            ".task-item"
                        );


                    if (taskItem) {


                        const taskTitle =
                            taskItem.querySelector(
                                ".task-title"
                            );


                        if (taskTitle) {


                            if (
                                taskTitle.classList.contains(
                                    "completed-task"
                                )
                            ) {

                                taskTitle.innerHTML =
                                    "✓ " +
                                    updatedTitle;

                            }
                            else {

                                taskTitle.textContent =
                                    updatedTitle;

                            }

                        }

                    }


                    // Update the title stored
                    // inside the button

                    button.setAttribute(
                        "data-task-title",
                        updatedTitle
                    );


                }
                catch (error) {


                    console.error(
                        "Edit task error:",
                        error
                    );


                    alert(
                        "Something went wrong."
                    );

                }

            }
        );

    }
);

