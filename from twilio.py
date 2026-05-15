using UnityEngine;

public class SimplePlayerController : MonoBehaviour
{
    [Header("Movement Settings")]
    public float speed = 8f;
    public float gravity = -9.81f;
    public CharacterController controller;

    [Header("Camera Settings")]
    public Camera playerCamera;
    public float mouseSensitivity = 200f;
    float xRotation = 0f;

    [Header("Combat Settings")]
    public float range = 100f;

    Vector3 velocity;

    void Start()
    {
        // Mouse ko game window mein lock karne ke liye
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update()
    {
        // 1. LOOK LOGIC (Aas paas dekhna)
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

        xRotation -= mouseY;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);

        playerCamera.transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
        transform.Rotate(Vector3.up * mouseX);

        // 2. MOVEMENT LOGIC (Chalna)
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");

        Vector3 move = transform.right * x + transform.forward * z;
        controller.Move(move * speed * Time.deltaTime);

        // Gravity apply karna
        velocity.y += gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);

        // 3. SHOOT LOGIC (Goli chalana)
        if (Input.GetButtonDown("Fire1")) // Mouse Left Click
        {
            Shoot();
        }
    }

    void Shoot()
    {
        RaycastHit hit;
        // Screen ke center se ray nikalna
        if (Physics.Raycast(playerCamera.transform.position, playerCamera.transform.forward, out hit, range))
        {
            Debug.Log("Goli Lagi: " + hit.transform.name);
            // Yahan par aap dushman ko damage dene ka logic likh sakte hain
        }
    }
}