import { useState } from "react";
import { useNavigate } from "react-router";
import "../styles/settings.css"
import { changePassword, deleteAccount } from "../api/user";

export default function SettingsPage() {
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageChange, setMessageChange] = useState("");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState("");

  const handleChangePassword = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      return setMessageChange("The passwords don't match");
    }

    try {
      await changePassword(currentPassword, newPassword);
      setMessageChange('');
      alert("The password has been changed")
    } catch (err) {
      setMessageChange(err.message);
    } finally {
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    }
  };

  const handleInitialDeleteClick = () => {
    setShowDeleteConfirm(true);
    setMessage("Are you sure you want to delete the account?");
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteAccount();
      setMessage("Konto zostało usunięte.");
      navigate("/register");
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <>
      <h2>Account Settings</h2>

      <div className="settings-container">
        <form onSubmit={handleChangePassword} className="settings-tile">
          <h3>Change password</h3>
          <label className="form-label">Current password
            <input 
              type="password"
              placeholder="Current password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required 
              className="form-input"
            />
          </label>
          <label className="form-label">New password
            <input 
              type="password"
              placeholder="New password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              className="form-input"
            />
          </label>
          <label className="form-label">Confirm new password
            <input
              type="password"
              placeholder="Repeat new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="form-input"
            />
            <p className="comment">{messageChange}</p>
          </label>
          
          <button type="submit" className="form-btn">Change password</button>
        </form>

        <div className="settings-tile">
          <h3>Delete account</h3>
          {!showDeleteConfirm ? (
            <button onClick={handleInitialDeleteClick} className="form-btn">
              Delete account
            </button>
          ) : (
            <>
              <p className="danger">{message}</p>
              <button onClick={handleConfirmDelete} className="form-btn">
                Confirm deletion
              </button>
            </>
          )}
        </div>
      </div>
    </>
  );
}
