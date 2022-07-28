import requests

from .utils import (
    API_ROOT,
    PULP_API_ROOT,
    CONTAINER_IMAGE,
    assert_pass,
    gen_string,
    del_registry,
    del_container,
    gen_registry,
    gen_remote_container,
    cleanup_test_obj
)

IMAGE_NAME = CONTAINER_IMAGE[0]


# REMOTES
def create_ee_remote(user, password, expect_pass, extra):
    registry = extra["registry"].get_registry()

    response = requests.post(
        f"{API_ROOT}_ui/v1/execution-environments/remotes/",
        json={
            "name": gen_string(),
            "upstream_name": "foo",
            "registry": registry["pk"],
        },
        auth=(user['username'], password),
    )

    cleanup_test_obj(response, "name", del_container)

    assert_pass(expect_pass, response.status_code, 201, 403)


def update_ee_remote(user, password, expect_pass, extra):
    remote = extra["remote_ee"].get_remote()
    remote["include_tags"] = ["latest"]

    response = requests.put(
        f"{API_ROOT}_ui/v1/execution-environments/remotes/{remote['pulp_id']}/",
        json=remote,
        auth=(user['username'], password),
    )

    assert_pass(expect_pass, response.status_code, 200, 403)


def sync_remote_ee(user, password, expect_pass, extra):
    container = extra["remote_ee"].get_container()

    response = requests.post(
        f'{API_ROOT}_ui/v1/execution-environments/repositories/{container["name"]}/_content/sync/',
        auth=(user['username'], password)
    )
    assert_pass(expect_pass, response.status_code, 202, 403)


# REGISTRIES
def delete_ee_registry(user, password, expect_pass, extra):
    registry = gen_registry(gen_string())

    response = requests.delete(
        f"{API_ROOT}_ui/v1/execution-environments/registries/{registry['pk']}/",
        auth=(user['username'], password),
    )

    del_registry(registry["pk"])

    assert_pass(expect_pass, response.status_code, 204, 403)


def index_ee_registry(user, password, expect_pass, extra):
    registry = extra["registry"].get_registry()

    response = requests.post(
        f"{API_ROOT}_ui/v1/execution-environments/registries/{registry['pk']}/index/",
        auth=(user['username'], password),
    )
    assert_pass(expect_pass, response.status_code, 400, 403)


def update_ee_registry(user, password, expect_pass, extra):
    registry = extra["registry"].get_registry()

    registry['rate_limit'] = 2

    response = requests.put(
        f"{API_ROOT}_ui/v1/execution-environments/registries/{registry['pk']}/",
        json=registry,
        auth=(user['username'], password),
    )
    assert_pass(expect_pass, response.status_code, 200, 403)


def create_ee_registry(user, password, expect_pass, extra):
    response = requests.post(
        f"{API_ROOT}_ui/v1/execution-environments/registries/",
        json={
            "name": gen_string(),
            "url": "http://example.com",
        },
        auth=(user['username'], password),
    )

    cleanup_test_obj(response, "pk", del_registry)

    assert_pass(expect_pass, response.status_code, 201, 403)


# EXECUTION ENVIRONMENTS
def delete_ee(user, password, expect_pass, extra):
    registry = extra["registry"].get_registry()

    name = gen_string()
    gen_remote_container(name, registry["pk"])

    response = requests.delete(
        f"{API_ROOT}_ui/v1/execution-environments/repositories/{name}/",
        auth=(user['username'], password),
    )

    del_container(name)

    assert_pass(expect_pass, response.status_code, 202, 403)


def change_ee_description(user, password, expect_pass, extra):
    container = extra["remote_ee"].get_container()

    response = requests.patch(
        f"{PULP_API_ROOT}distributions/container/container/{container['id']}/",
        json={
            "description": "hello world",
        },
        auth=(user['username'], password),
    )
    assert_pass(expect_pass, response.status_code, 202, 403)


def change_ee_readme(user, password, expect_pass, extra):
    container = extra["remote_ee"].get_container()

    url = (
        f"{API_ROOT}_ui/v1/execution-environments/repositories/"
        f"{container['name']}/_content/readme/"
    )
    response = requests.put(
        url,
        json={"text": "Praise the readme!"},
        auth=(user['username'], password),
    )
    assert_pass(expect_pass, response.status_code, 200, 403)


def change_ee_namespace(user, password, expect_pass, extra):
    namespace = extra["remote_ee"].get_namespace()

    response = requests.put(
        f"{API_ROOT}_ui/v1/execution-environments/namespaces/{namespace['name']}/",
        json=namespace,
        auth=(user['username'], password)
    )

    assert_pass(expect_pass, response.status_code, 200, 403)


def create_ee_local(user, password, expect_pass, extra):
    # waiting on pulp container fix
    pass

    # return_code = podman_login(user['username'], password)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(user['username'], index=0)
    # if return_code == 0:
    #     return_code = podman_push(tag=user['username'], index=0)
    # if expect_pass:
    #     assert return_code == 0
    # else:
    #     assert return_code != 0


def create_ee_in_existing_namespace(user, password, expect_pass, extra):
    # waiting on pulp container fix
    pass

    # return_code = podman_login(ADMIN_USER, ADMIN_PASSWORD)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(tag=user['username'], index=0)
    # if return_code == 0:
    #     return_code = podman_push(tag=ADMIN_USER, index=0)

    # # push new container to existing namespace
    # return_code = podman_login(user['username'], password)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(tag=user['username'], index=1)
    # if return_code == 0:
    #     return_code = podman_push(tag=user['username'], index=1)

    # if expect_pass:
    #     assert return_code == 0
    # else:
    #     assert return_code != 0


def push_updates_to_existing_ee(user, password, expect_pass, extra):
    # waiting on pulp container fix
    pass

    # # create container
    # return_code = podman_login(ADMIN_USER, ADMIN_PASSWORD)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(tag=ADMIN_USER, index=0)
    # if return_code == 0:
    #     return_code = podman_push(tag=ADMIN_USER, index=0)

    # # repush existing container
    # return_code = podman_login(user['username'], password)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(tag=user['username'], index=0)
    # if return_code == 0:
    #     return_code = podman_push(tag=user, index=0)
    # if expect_pass:
    #     assert return_code == 0
    # else:
    #     assert return_code != 0


def change_ee_tags(user, password, expect_pass, extra):
    # waiting on pulp container fix
    pass

    # # create container namespace
    # return_code = podman_login(ADMIN_USER, ADMIN_PASSWORD)
    # if return_code == 0:
    #     return_code = podman_build_and_tag(tag=user['username'], index=0)
    # if return_code == 0:
    #     return_code = podman_push(tag=ADMIN_USER, index=0)

    # # get image & push container data
    # image_data = get_container_image_data()
    # push_container_pk = get_push_container_pk()
    # # Tag
    # response = requests.post(
    #     f'{PULP_API_ROOT}repositories/container/container-push/{push_container_pk}/tag/',
    #     json={
    #         'digest': image_data['digest'],
    #         'tag': user['username']
    #     },
    #     auth=(user['username'], password)
    # )
    # assert_pass(expect_pass, response.status_code, 202, 403)
    # if response.status_code == 202:
    #     wait_for_task(response)

    # # Untag
    # response = requests.post(
    #     f'{PULP_API_ROOT}repositories/container/container-push/{push_container_pk}/untag/',
    #     json={'tag': user['username']},
    #     auth=(user['username'], password)
    # )
    # assert_pass(expect_pass, response.status_code, 202, 403)
    # if response.status_code == 202:
    #     wait_for_task(response)
