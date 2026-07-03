import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getUsers,
  createUser,
  getRoles,
  createRole,
  getPermissions,
  createPermission,
  getCapabilities,
  createCapability,
  getAreas,
  createArea,
  getTeams,
  createTeam,
  assignRoleToUser,
  assignTeamToUser,
  assignPermissionToRole,
  assignCapabilityToRole,
} from "./iamApi.js";

import "../../../components/forms/forms.css";

function IAMPage() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [areas, setAreas] = useState([]);
  const [teams, setTeams] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [userForm, setUserForm] = useState({
    username: "",
    password: "",
    full_name: "",
    email: "",
    role: "analyst",
    area: "",
    is_active: true,
    is_superuser: false,
  });

  const [roleForm, setRoleForm] = useState({
    code: "",
    name: "",
    description: "",
    is_active: true,
  });

  const [permissionForm, setPermissionForm] = useState({
    code: "",
    name: "",
    description: "",
    category: "",
    is_active: true,
  });

  const [capabilityForm, setCapabilityForm] = useState({
    code: "",
    name: "",
    description: "",
    is_active: true,
  });

  const [areaForm, setAreaForm] = useState({
    code: "",
    name: "",
    description: "",
    is_active: true,
  });

  const [teamForm, setTeamForm] = useState({
    code: "",
    name: "",
    area_id: "",
    description: "",
    is_active: true,
  });

  const [assignForm, setAssignForm] = useState({
    user_id: "",
    role_id: "",
    team_id: "",
    permission_role_id: "",
    permission_id: "",
    capability_role_id: "",
    capability_id: "",
  });

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        usersResponse,
        rolesResponse,
        permissionsResponse,
        capabilitiesResponse,
        areasResponse,
        teamsResponse,
      ] = await Promise.all([
        getUsers(),
        getRoles(),
        getPermissions(),
        getCapabilities(),
        getAreas(),
        getTeams(),
      ]);

      setUsers(usersResponse.data);
      setRoles(rolesResponse.data);
      setPermissions(permissionsResponse.data);
      setCapabilities(capabilitiesResponse.data);
      setAreas(areasResponse.data);
      setTeams(teamsResponse.data);
    } catch (err) {
      setError(err.message || "Error cargando IAM");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUserChange = (event) => {
    const { name, value, type, checked } = event.target;

    setUserForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleGenericChange = (setter) => (event) => {
    const { name, value, type, checked } = event.target;

    setter((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleAssignChange = (event) => {
    const { name, value } = event.target;

    setAssignForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleCreateUser = async (event) => {
    event.preventDefault();

    await createUser(userForm);

    setUserForm({
      username: "",
      password: "",
      full_name: "",
      email: "",
      role: "analyst",
      area: "",
      is_active: true,
      is_superuser: false,
    });

    loadData();
  };

  const handleCreateRole = async (event) => {
    event.preventDefault();

    await createRole(roleForm);

    setRoleForm({
      code: "",
      name: "",
      description: "",
      is_active: true,
    });

    loadData();
  };

  const handleCreatePermission = async (event) => {
    event.preventDefault();

    await createPermission(permissionForm);

    setPermissionForm({
      code: "",
      name: "",
      description: "",
      category: "",
      is_active: true,
    });

    loadData();
  };

  const handleCreateCapability = async (event) => {
    event.preventDefault();

    await createCapability(capabilityForm);

    setCapabilityForm({
      code: "",
      name: "",
      description: "",
      is_active: true,
    });

    loadData();
  };

  const handleCreateArea = async (event) => {
    event.preventDefault();

    await createArea(areaForm);

    setAreaForm({
      code: "",
      name: "",
      description: "",
      is_active: true,
    });

    loadData();
  };

  const handleCreateTeam = async (event) => {
    event.preventDefault();

    await createTeam({
      ...teamForm,
      area_id: teamForm.area_id ? Number(teamForm.area_id) : null,
    });

    setTeamForm({
      code: "",
      name: "",
      area_id: "",
      description: "",
      is_active: true,
    });

    loadData();
  };

  const handleAssignRoleToUser = async (event) => {
    event.preventDefault();

    await assignRoleToUser({
      user_id: Number(assignForm.user_id),
      role_id: Number(assignForm.role_id),
    });

    loadData();
  };

  const handleAssignTeamToUser = async (event) => {
    event.preventDefault();

    await assignTeamToUser({
      user_id: Number(assignForm.user_id),
      team_id: Number(assignForm.team_id),
    });

    loadData();
  };

  const handleAssignPermissionToRole = async (event) => {
    event.preventDefault();

    await assignPermissionToRole({
      role_id: Number(assignForm.permission_role_id),
      permission_id: Number(assignForm.permission_id),
    });

    loadData();
  };

  const handleAssignCapabilityToRole = async (event) => {
    event.preventDefault();

    await assignCapabilityToRole({
      role_id: Number(assignForm.capability_role_id),
      capability_id: Number(assignForm.capability_id),
    });

    loadData();
  };

  return (
    <>
      <PageHeader
        title="IAM"
        description="Usuarios, roles, permisos, capacidades, áreas y equipos."
      />

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      <Card title="Crear usuario">
        <form onSubmit={handleCreateUser} className="simple-form">
          <label>
            Usuario
            <input name="username" value={userForm.username} onChange={handleUserChange} required />
          </label>

          <label>
            Contraseña
            <input type="password" name="password" value={userForm.password} onChange={handleUserChange} required />
          </label>

          <label>
            Nombre completo
            <input name="full_name" value={userForm.full_name} onChange={handleUserChange} />
          </label>

          <label>
            Email
            <input name="email" value={userForm.email} onChange={handleUserChange} />
          </label>

          <label>
            Rol legado
            <select name="role" value={userForm.role} onChange={handleUserChange}>
              <option value="admin">Admin</option>
              <option value="supervisor">Supervisor</option>
              <option value="analyst">Analista</option>
              <option value="quality">Calidad</option>
              <option value="viewer">Consulta</option>
            </select>
          </label>

          <label>
            Área
            <input name="area" value={userForm.area} onChange={handleUserChange} />
          </label>

          <label className="checkbox-row">
            <input type="checkbox" name="is_active" checked={userForm.is_active} onChange={handleUserChange} />
            Activo
          </label>

          <label className="checkbox-row">
            <input type="checkbox" name="is_superuser" checked={userForm.is_superuser} onChange={handleUserChange} />
            Superusuario
          </label>

          <div className="form-actions">
            <Button type="submit">Crear usuario</Button>
          </div>
        </form>
      </Card>

      <Card title="Usuarios">
        <DataTable
          columns={[
            { key: "id", label: "ID" },
            { key: "username", label: "Usuario" },
            { key: "full_name", label: "Nombre" },
            { key: "role", label: "Rol legado" },
            { key: "area", label: "Área" },
            {
              key: "is_active",
              label: "Activo",
              render: (row) => (row.is_active ? "Sí" : "No"),
            },
            {
              key: "is_superuser",
              label: "Super",
              render: (row) => (row.is_superuser ? "Sí" : "No"),
            },
          ]}
          data={users}
          emptyMessage="No hay usuarios."
        />
      </Card>

      <Card title="Crear rol">
        <form onSubmit={handleCreateRole} className="simple-form">
          <label>
            Código
            <input name="code" value={roleForm.code} onChange={handleGenericChange(setRoleForm)} required />
          </label>

          <label>
            Nombre
            <input name="name" value={roleForm.name} onChange={handleGenericChange(setRoleForm)} required />
          </label>

          <label>
            Descripción
            <textarea name="description" value={roleForm.description} onChange={handleGenericChange(setRoleForm)} />
          </label>

          <label className="checkbox-row">
            <input type="checkbox" name="is_active" checked={roleForm.is_active} onChange={handleGenericChange(setRoleForm)} />
            Activo
          </label>

          <div className="form-actions">
            <Button type="submit">Crear rol</Button>
          </div>
        </form>
      </Card>

      <Card title="Roles">
        <DataTable
          columns={[
            { key: "id", label: "ID" },
            { key: "code", label: "Código" },
            { key: "name", label: "Nombre" },
            { key: "description", label: "Descripción" },
          ]}
          data={roles}
          emptyMessage="No hay roles."
        />
      </Card>

      <Card title="Permisos y capacidades">
        <div className="simple-form">
          <form onSubmit={handleCreatePermission}>
            <label>
              Código permiso
              <input name="code" value={permissionForm.code} onChange={handleGenericChange(setPermissionForm)} required />
            </label>

            <label>
              Nombre
              <input name="name" value={permissionForm.name} onChange={handleGenericChange(setPermissionForm)} required />
            </label>

            <label>
              Categoría
              <input name="category" value={permissionForm.category} onChange={handleGenericChange(setPermissionForm)} />
            </label>

            <div className="form-actions">
              <Button type="submit">Crear permiso</Button>
            </div>
          </form>

          <form onSubmit={handleCreateCapability}>
            <label>
              Código capacidad
              <input name="code" value={capabilityForm.code} onChange={handleGenericChange(setCapabilityForm)} required />
            </label>

            <label>
              Nombre
              <input name="name" value={capabilityForm.name} onChange={handleGenericChange(setCapabilityForm)} required />
            </label>

            <label>
              Descripción
              <input name="description" value={capabilityForm.description} onChange={handleGenericChange(setCapabilityForm)} />
            </label>

            <div className="form-actions">
              <Button type="submit">Crear capacidad</Button>
            </div>
          </form>
        </div>
      </Card>

      <Card title="Permisos">
        <DataTable
          columns={[
            { key: "id", label: "ID" },
            { key: "code", label: "Código" },
            { key: "name", label: "Nombre" },
            { key: "category", label: "Categoría" },
          ]}
          data={permissions}
          emptyMessage="No hay permisos."
        />
      </Card>

      <Card title="Capacidades">
        <DataTable
          columns={[
            { key: "id", label: "ID" },
            { key: "code", label: "Código" },
            { key: "name", label: "Nombre" },
          ]}
          data={capabilities}
          emptyMessage="No hay capacidades."
        />
      </Card>

      <Card title="Áreas y equipos">
        <div className="simple-form">
          <form onSubmit={handleCreateArea}>
            <label>
              Código área
              <input name="code" value={areaForm.code} onChange={handleGenericChange(setAreaForm)} required />
            </label>

            <label>
              Nombre área
              <input name="name" value={areaForm.name} onChange={handleGenericChange(setAreaForm)} required />
            </label>

            <div className="form-actions">
              <Button type="submit">Crear área</Button>
            </div>
          </form>

          <form onSubmit={handleCreateTeam}>
            <label>
              Código equipo
              <input name="code" value={teamForm.code} onChange={handleGenericChange(setTeamForm)} required />
            </label>

            <label>
              Nombre equipo
              <input name="name" value={teamForm.name} onChange={handleGenericChange(setTeamForm)} required />
            </label>

            <label>
              Área
              <select name="area_id" value={teamForm.area_id} onChange={handleGenericChange(setTeamForm)}>
                <option value="">Sin área</option>
                {areas.map((area) => (
                  <option key={area.id} value={area.id}>
                    {area.name}
                  </option>
                ))}
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Crear equipo</Button>
            </div>
          </form>
        </div>
      </Card>

      <Card title="Asignaciones">
        <div className="simple-form">
          <form onSubmit={handleAssignRoleToUser}>
            <label>
              Usuario
              <select name="user_id" value={assignForm.user_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Rol
              <select name="role_id" value={assignForm.role_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name}
                  </option>
                ))}
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Asignar rol</Button>
            </div>
          </form>

          <form onSubmit={handleAssignTeamToUser}>
            <label>
              Usuario
              <select name="user_id" value={assignForm.user_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Equipo
              <select name="team_id" value={assignForm.team_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Asignar equipo</Button>
            </div>
          </form>

          <form onSubmit={handleAssignPermissionToRole}>
            <label>
              Rol
              <select name="permission_role_id" value={assignForm.permission_role_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Permiso
              <select name="permission_id" value={assignForm.permission_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {permissions.map((permission) => (
                  <option key={permission.id} value={permission.id}>
                    {permission.code}
                  </option>
                ))}
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Asignar permiso</Button>
            </div>
          </form>

          <form onSubmit={handleAssignCapabilityToRole}>
            <label>
              Rol
              <select name="capability_role_id" value={assignForm.capability_role_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Capacidad
              <select name="capability_id" value={assignForm.capability_id} onChange={handleAssignChange} required>
                <option value="">Seleccione...</option>
                {capabilities.map((capability) => (
                  <option key={capability.id} value={capability.id}>
                    {capability.code}
                  </option>
                ))}
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Asignar capacidad</Button>
            </div>
          </form>
        </div>
      </Card>
    </>
  );
}

export default IAMPage;
