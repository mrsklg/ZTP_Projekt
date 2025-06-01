import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import RegisterForm from "../components/RegisterForm";
import { registerUser } from "../api/auth";
import { MemoryRouter } from "react-router";

// Mockujemy registerUser
jest.mock("../api/auth", () => ({
  registerUser: jest.fn(),
}));

// Mockujemy useNavigate z react-router-dom
const mockedNavigate = jest.fn();

jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useNavigate: () => mockedNavigate,
}));

describe("RegisterForm", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders all input fields and the submit button", () => {
    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    expect(screen.getByPlaceholderText("Name")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Surname")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Email")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /register/i })).toBeInTheDocument();
  });

  test("updates input values on change", () => {
    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    const nameInput = screen.getByPlaceholderText("Name");
    const surnameInput = screen.getByPlaceholderText("Surname");
    const emailInput = screen.getByPlaceholderText("Email");
    const passwordInput = screen.getByPlaceholderText("Password");

    fireEvent.change(nameInput, { target: { value: "Jan" } });
    fireEvent.change(surnameInput, { target: { value: "Kowalski" } });
    fireEvent.change(emailInput, { target: { value: "jan@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "123456" } });

    expect(nameInput.value).toBe("Jan");
    expect(surnameInput.value).toBe("Kowalski");
    expect(emailInput.value).toBe("jan@example.com");
    expect(passwordInput.value).toBe("123456");
  });

  test("calls registerUser and navigates on successful registration", async () => {
    registerUser.mockResolvedValue({ id: "123" });

    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Name"), { target: { value: "Jan" } });
    fireEvent.change(screen.getByPlaceholderText("Surname"), { target: { value: "Kowalski" } });
    fireEvent.change(screen.getByPlaceholderText("Email"), { target: { value: "jan@example.com" } });
    fireEvent.change(screen.getByPlaceholderText("Password"), { target: { value: "123456" } });

    fireEvent.submit(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(registerUser).toHaveBeenCalledWith("jan@example.com", "123456", "Jan", "Kowalski");
      expect(mockedNavigate).toHaveBeenCalledWith("/login");
    });
  });

  test("shows alert on registration failure", async () => {
    const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});
    registerUser.mockResolvedValue({ error: "Email already exists" });

    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Name"), { target: { value: "Jan" } });
    fireEvent.change(screen.getByPlaceholderText("Surname"), { target: { value: "Kowalski" } });
    fireEvent.change(screen.getByPlaceholderText("Email"), { target: { value: "jan@example.com" } });
    fireEvent.change(screen.getByPlaceholderText("Password"), { target: { value: "123456" } });

    fireEvent.submit(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(registerUser).toHaveBeenCalled();
      expect(alertMock).toHaveBeenCalledWith("Register failed: Email already exists");
      expect(mockedNavigate).not.toHaveBeenCalled();
    });

    alertMock.mockRestore();
  });
});
